# Create data directories
mkdir -p data/raw_data
mkdir -p data/proc_data

echo 'Downloading data...'

# Download & unzip data
curl https://www.ssa.gov/oact/babynames/names.zip -o data/raw_data/data.zip
unzip data/raw_data/data.zip -d data/raw_data/

echo 'Data downloaded'
echo 'Processing files...'

# Rename data files to remove 'yob' at the start of each filename
for file in data/raw_data/*.txt
do
    mv "${file}" "${file/yob/}"
done

# Add appropriate year to each line in each data file
for file in data/raw_data/*.txt
do
    year=$(basename $file .txt)
    sed 's/^/'"$year"',/' "$file" > data/proc_data/"$year".csv
done

# Concatenate data files together into a single
cat data/proc_data/*.csv > data/babynames.csv

echo 'Files processed'
echo 'Executing Python script...'

# Run Python processing script
python process_data.py