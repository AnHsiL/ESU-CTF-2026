"""Compare public-key/ciphertext lengths across TT, TF, FT, FF.

Usage: python graph_len.py [--no-show] [--csv FILE] [--output FILE]
Requires matplotlib. Input defaults to exp_capacity.csv beside this script.
"""
import argparse
import csv
from pathlib import Path

CASES = ('TT', 'TF', 'FT', 'FF')


def read_lengths(path):
    groups = {case: {} for case in CASES}
    message_sizes = set()
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        required = {'capacity_bytes', 'case', 'message_bytes',
                    'public_key_bytes', 'ciphertext_bytes'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f'CSV must contain {sorted(required)}')
        for line, row in enumerate(reader, 2):
            case = row['case'].strip()
            if case not in groups:
                raise ValueError(f'Line {line}: unknown case {case!r}')
            capacity, key_size, cipher_size, msg_size = (
                int(row[name]) for name in ('capacity_bytes', 'public_key_bytes',
                                           'ciphertext_bytes', 'message_bytes'))
            if min(capacity, key_size, cipher_size) < 1 or not 0 <= msg_size <= capacity:
                raise ValueError(f'Line {line}: invalid length')
            lengths = (key_size, cipher_size)
            previous = groups[case].get(capacity)
            # Repeated timing trials must agree in encoded byte length.
            if previous is not None and previous != lengths:
                raise ValueError(f'Inconsistent lengths: capacity={capacity}, case={case}')
            groups[case][capacity] = lengths
            message_sizes.add(msg_size)
    capacities = sorted(groups['TT'])
    if not capacities or any(sorted(group) != capacities for group in groups.values()):
        raise ValueError('All four cases must contain the same capacities')
    return groups, capacities, message_sizes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path,
                        default=Path(__file__).resolve().with_name('exp_capacity.csv'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--no-show', action='store_true')
    args = parser.parse_args()
    try:
        groups, capacities, message_sizes = read_lengths(args.csv)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    import matplotlib
    if args.no_show:
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    styles = [('o', '-', 11), ('s', '--', 8), ('^', '-.', 6), ('x', ':', 4)]
    for case, (marker, linestyle, size) in zip(CASES, styles):
        for column, ax in enumerate(axes):
            ax.plot(capacities, [groups[case][c][column] for c in capacities],
                    label=case, marker=marker, linestyle=linestyle,
                    markersize=size, markerfacecolor='none', linewidth=1.6)
    for column, ax in enumerate(axes):
        name = ('Public Key', 'Ciphertext')[column]
        ax.set_title(f'{name} Length')
        ax.set_xlabel('Capacity (bytes)')
        ax.set_ylabel(f'{name} length (bytes)')
        ax.set_xticks(capacities)
        ax.set_ylim(bottom=0)
        ax.ticklabel_format(axis='y', style='plain', useOffset=False)
        ax.grid(alpha=0.3)
        ax.legend(title='Sender / Receiver')
    equal = all(len({groups[case][c] for case in CASES}) == 1 for c in capacities)
    fig.suptitle('Encoded Length vs. Capacity')
    footer = ('All four cases have identical lengths; curves overlap.' if equal else
              'Lengths differ between cases; inspect the source data.')
    if len(message_sizes) == 1:
        footer += f' Input message: {next(iter(message_sizes))} byte(s).'
    fig.text(0.5, 0.015, footer, ha='center', fontsize=10)
    fig.tight_layout(rect=(0, 0.055, 1, 0.94))
    output = args.output or args.csv.resolve().with_name('capacity_length.png')
    fig.savefig(output, dpi=200)
    print(footer)
    print(f'Checked {len(capacities)} capacities across {len(CASES)} cases.')
    print(f'Saved: {output.resolve()}')
    if not args.no_show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    main()
