# Load required library
library(GenomicRanges)
library(stats4)


# Function to read BED file and coordinate list
read_bed_file <- function(filepath) {
  return(read.table(filepath, header = FALSE, stringsAsFactors = FALSE))
}

# Function to count overlaps
count_overlaps <- function(bed_file, coord_file) {
  bed_data <- read_bed_file(bed_file)
  coord_data <- read_bed_file(coord_file)

  gr_bed <- GRanges(seqnames = bed_data$V1, 
                    ranges = IRanges(start = bed_data$V2, end = bed_data$V3))

  gr_coord <- GRanges(seqnames = coord_data$V1, 
                      ranges = IRanges(start = coord_data$V2, end = coord_data$V3))

  overlap_counts <- countOverlaps(gr_bed, gr_coord)
  
  result_df <- cbind(bed_data, count = overlap_counts)
  
  return(result_df)
}

# Main execution
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop("Usage: Rscript intersect.R <bed_file> <coord_file> <output_file>")
}

bed_file <- args[1]
coord_file <- args[2]
output_file <- args[3]

# Count overlaps and write to output file
overlap_results <- count_overlaps(bed_file, coord_file)
write.table(overlap_results, output_file, sep = "\t", quote = FALSE, row.names = FALSE, col.names = FALSE)
cat("Overlap counts written to:", output_file, "\n")