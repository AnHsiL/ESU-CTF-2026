"""Plot capacity against time for TT/TF/FT/FF. Requires matplotlib.

python graph.py
python graph.py --metric send
python graph.py --metric receive --no-show
"""
import argparse
import csv
import math
from pathlib import Path

CASES = ('TT', 'TF', 'FT', 'FF')


def read_data(path, metric):
    column = f'{metric}_seconds'
    groups = {case: [] for case in CASES}
    seen = set()
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        required = {'capacity_bytes', 'case', column}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f'CSV must contain: {sorted(required)}')
        for line, row in enumerate(reader, start=2):
            case = row['case'].strip()
            if case not in groups:
                raise ValueError(f'Line {line}: unknown case {case!r}')
            capacity = int(row['capacity_bytes'])
            seconds = float(row[column])
            if capacity < 1 or not math.isfinite(seconds) or seconds < 0:
                raise ValueError(f'Line {line}: invalid capacity or time')
            key = (case, capacity)
            if key in seen:
                raise ValueError(f'Duplicate measurement {key}; aggregate repeats first')
            seen.add(key)
            groups[case].append((capacity, seconds))
    if any(not points for points in groups.values()):
        raise ValueError('CSV must contain all four cases: TT, TF, FT, FF')
    for points in groups.values():
        points.sort()
    return groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path,
                        default=Path(__file__).resolve().with_name('exp_capacity.csv'))
    parser.add_argument('--metric', choices=('total', 'start', 'send', 'receive'),
                        default='total', help='Time column to plot (default: total)')
    parser.add_argument('--output', type=Path, help='PNG output path')
    parser.add_argument('--no-show', action='store_true', help='Save without opening a window')
    args = parser.parse_args()
    try:
        groups = read_data(args.csv, args.metric)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    import matplotlib
    if args.no_show:
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 5.5))
    styles = [('o', '-'), ('s', '--'), ('^', '-.'), ('D', ':')]
    for case, (marker, style) in zip(CASES, styles):
        capacities, seconds = zip(*groups[case])
        ax.plot(capacities, seconds, label=case, marker=marker,
                linestyle=style, linewidth=1.8, markersize=5)
    ticks = sorted({capacity for points in groups.values() for capacity, _ in points})
    ax.set_xticks(ticks)
    ax.set_xlabel('Capacity (bytes)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title(f'Capacity vs. {args.metric.capitalize()} Time')
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    ax.legend(title='Sender / Receiver')
    fig.tight_layout()
    output = args.output or args.csv.resolve().with_name(f'capacity_{args.metric}.png')
    fig.savefig(output, dpi=200)
    print(f'Saved: {output.resolve()}')
    if not args.no_show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    main()
