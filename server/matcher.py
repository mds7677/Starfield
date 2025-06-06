from sklearn.neighbors import KDTree 
from itertools import combinations
from collections import Counter
from datetime import datetime
import pandas as pd
import numpy as np
import cv2

from data.constellation import constellation_names
from constellation_lines import lines

metrics = pd.read_csv('data/triangles.csv')
tree = KDTree(metrics[['angle1', 'angle2', 'angle3']])


def format_log_message(message: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {message}\n"

def distance(a: pd.DataFrame, b: pd.DataFrame) -> float:
    return np.sqrt(
        (a['x'].values[0] - b['x'].values[0]) ** 2
         + (a['y'].values[0] - b['y'].values[0]) ** 2
    )

def calculate_2d_triangle_angles(side_ab: float, side_bc: float, side_ac: float) -> np.ndarray:
    cos_A = (side_bc**2 + side_ac**2 - side_ab**2) / (2 * side_bc * side_ac)
    cos_B = (side_ab**2 + side_ac**2 - side_bc**2) / (2 * side_ab * side_ac)
    cos_C = (side_ab**2 + side_bc**2 - side_ac**2) / (2 * side_ab * side_bc)
    
    angles = np.degrees([
        np.arccos(np.clip(cos_A, -1.0, 1.0)),
        np.arccos(np.clip(cos_B, -1.0, 1.0)),
        np.arccos(np.clip(cos_C, -1.0, 1.0))
    ])
    return np.sort(angles)

def find_stars(path: str) -> tuple[list[tuple[float, float]], str]:
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, ksize=3)
    _, thresh = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    star_coords = []
    img_with_stars = img.copy()
    log_str = ""

    for ind, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 0:
            moments = cv2.moments(contour)
            if moments['m00'] != 0:
                x = int(moments['m10']/moments['m00'])
                y = int(moments['m01']/moments['m00'])
                star_coords.append((x, y))
                cv2.rectangle(img_with_stars, (x-7, y-7), (x+7, y+7), (0, 0, 255), 1)
                cv2.putText(img_with_stars, f"{ind}", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0, 0, 255), 2)

    star_image_path = f'examples/logs/detected_{path.split("/")[-1]}'
    cv2.imwrite(star_image_path, img_with_stars)
    log_str += format_log_message(f"Detected {len(star_coords)} stars in {path}. Saved marked stars image to {star_image_path}")

    return star_coords, log_str

def find_lines(matches, lines, dots):
    pairs_to_draw = []
    name_votes = []
    used_hips = set(matches.values())
    log_str = ""

    for i, j in combinations(range(len(matches)), 2):
        dot_1 = matches[i]
        dot_2 = matches[j]
        if dot_1 == dot_2:
            continue
        for constellation, pairs in lines.items():
            for pair in pairs:
                if dot_1 in pair and dot_2 in pair:
                    name_votes.append(constellation)
                    pairs_to_draw.append([dots[i], dots[j]])

    if not name_votes:
        log_str += format_log_message("No constellation identified.")
        return None, [], log_str
    
    name = Counter(name_votes).most_common(1)[0][0]
    constellation_hips = set()
    for pair in lines.get(name, []):
        constellation_hips.update(pair)

    fake_stars = [(i, hip) for i, hip in matches.items() if hip not in constellation_hips]
    if fake_stars:
        log_str += format_log_message(f"Suspected fake stars (index, HIP): {fake_stars}")

    log_str += format_log_message(f"Identified constellation: {name} with {len(pairs_to_draw)} line pairs.")
    return name, pairs_to_draw, log_str

def draw_lines(lines_to_draw, name: str, path: str):
    img = cv2.imread(path)
    for pair in lines_to_draw:
        dot_1, dot_2 = pair[0], pair[1]
        cv2.line(img, dot_1, dot_2, (255, 255, 0), 1)
    output_path = f'examples/results/{name.lower()}.jpg'
    cv2.imwrite(output_path, img)


def choose_best_hip(idx: int, candidates: list[float],
                    distances: dict[float, list[float]],
                    used_hips: set[float]) -> tuple[float | None, str]: # updated
    log_str = ""
    if not candidates:
        return None, log_str

    counter = Counter(candidates)
    most_common = counter.most_common()
    top_votes = most_common[0][1]
    top_candidates = [hip for hip, votes in most_common if votes == top_votes and hip not in used_hips]

    if not top_candidates:
        return None, log_str

    if len(top_candidates) == 1:
        chosen = top_candidates[0]
    else:
        chosen = min(top_candidates, key=lambda hip: np.mean(distances[hip]))
        log_str += format_log_message(f"Resolved tie for star {idx} among HIPs {top_candidates} by choosing {chosen} with min mean distance {np.mean(distances[chosen]):.4f}")
    return chosen, log_str

def match_stars_to_catalogue(df: pd.DataFrame, metrics: pd.DataFrame, tree: KDTree) -> tuple[dict[int, float], str]: # updated
    used_hips: set[float] = set()
    matches: dict[int, float] = {}
    log_str = ""

    for i in range(len(df)):
        dot_1 = df.iloc[[i]]
        hip_distances: dict[float, list[float]] = {}
        hip_candidates: list[float] = []

        for j, k in combinations(range(len(df)), 2):
            if i in [j, k]:
                continue

            dot_2 = df.iloc[[j]]
            dot_3 = df.iloc[[k]]

            AB = distance(dot_1, dot_2)
            BC = distance(dot_2, dot_3)
            AC = distance(dot_1, dot_3)

            angles = calculate_2d_triangle_angles(AB, BC, AC)
            dist, ind = tree.query([angles], k=2)

            for idx, d in zip(ind[0], dist[0]):
                triangle = metrics.iloc[idx]
                hips = [triangle['hip1'], triangle['hip2'], triangle['hip3']]
                for hip in hips:
                    if hip in used_hips:
                        continue
                    hip_candidates.append(hip)
                    hip_distances.setdefault(hip, []).append(d)

        best_hip, hip_log = choose_best_hip(i, hip_candidates, hip_distances, used_hips)
        log_str += hip_log
        if best_hip is not None:
            matches[i] = float(best_hip)
            used_hips.add(best_hip)

    log_str += format_log_message(f"Matched {len(matches)} stars to catalog HIP numbers.")
    return matches, log_str


def match(import_path: str) -> tuple[str, list[list], str]:
    log_str = ""
    dots, log_img_processing = find_stars(import_path)
    log_str += log_img_processing
    df = pd.DataFrame(dots, columns=["x", "y"])
    matches, log_matching = match_stars_to_catalogue(df, metrics, tree)
    log_str += log_matching

    short_name, output_list, log_lines = find_lines(matches, lines, dots)
    log_str += log_lines
    full_name = constellation_names.get(short_name, short_name)
    return full_name, output_list, log_str

# match('examples/inputs/image1.png', 'example.jpg')