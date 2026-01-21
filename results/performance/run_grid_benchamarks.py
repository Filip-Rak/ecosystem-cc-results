import shutil
import subprocess
from pathlib import Path
from PIL import Image

PROGRAM = "ecosystem.exe"

# ( width/height , agents )
TESTS = [
    (100, 500), (200, 1000), (400, 2000), (1000, 5000),
    (100, 0),   (200, 0),    (400, 0),    (1000, 0),
]

# solid grayscale shades (0..255)
SHADES = {
    "temperature.png": 128,
    "humidity.png": 128,
    "elevation.png": 20,
    "population.png": 0,
}

GRID_DIR = Path( "grid" )

def make_images( size: int ):
    GRID_DIR.mkdir( exist_ok=True )
    for name, shade in SHADES.items():
        Image.new( "L", ( size, size ), shade ).save( GRID_DIR / name )


def main():
    for size, agents in TESTS:
        shutil.rmtree( GRID_DIR, ignore_errors=True )
        make_images( size )

        cmd = [
            PROGRAM,
            "--test-performance",
            "--tlog", "1000000",
            "--preset", "benchmarkPreset.json",
            "--agents", str( agents ),
            "--output", f"output{size}x{size}-{agents}/",
        ]

        print( "Running:", " ".join(cmd) )
        subprocess.run( cmd, check=True )

    shutil.rmtree( GRID_DIR, ignore_errors=True )

if __name__ == "__main__":
    main()
