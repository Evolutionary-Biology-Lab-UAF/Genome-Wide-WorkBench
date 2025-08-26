# # # Load required libraries
# # library(RIdeogram)
# # library(Cairo)
# # library(rsvg)
# # library(data.table)

# # # Get command line arguments
# # args <- commandArgs(trailingOnly = TRUE)

# # # Check if the correct number of arguments are provided
# # if (length(args) < 3) {
# #   stop("Usage: Rscript generate_ideogram.R <karyotype_csv> <gene_density_csv> <output_dir>")
# # }

# # # Load data
# # human_karyotype <- fread(args[1], sep = ",", header = TRUE, stringsAsFactors = FALSE)
# # gene_density <- fread(args[2], sep = ",", header = TRUE, stringsAsFactors = FALSE)

# # # Verify data
# # cat("Preview of Karyotype Data:\n")
# # print(head(human_karyotype))
# # cat("Preview of Gene Density Data:\n")
# # print(head(gene_density))

# # # Specify output directory
# # output_dir <- args[3]

# # # Create output directory if it doesn't exist
# # if (!dir.exists(output_dir)) {
# #   dir.create(output_dir, recursive = TRUE)
# # }

# # # Generate ideogram
# # svg_file <- file.path(output_dir, "chromosome.svg")
# # ideogram(
# #   karyotype = human_karyotype,
# #   overlaid = gene_density,
# #   colorset1 = topo.colors(10),
# #   colorset2 = terrain.colors(10),
# #   output = svg_file
# # )

# # # Check if SVG was created
# # if (file.exists(svg_file)) {
# #   cat("Ideogram SVG file generated successfully at:", svg_file, "\n")
# # } else {
# #   stop("Error: SVG file not created.")
# # }
# # Load required libraries
# library(RIdeogram)
# library(Cairo)
# library(rsvg)
# library(data.table)

# # Get command line arguments
# args <- commandArgs(trailingOnly = TRUE)

# # Check if the correct number of arguments are provided
# if (length(args) < 3) {
#   stop("Usage: Rscript generate_ideogram.R <karyotype_csv> <gene_density_csv> <output_dir>")
# }

# # Load data
# human_karyotype <- fread(args[1], sep = ",", header = TRUE, stringsAsFactors = FALSE)
# gene_density <- fread(args[2], sep = ",", header = TRUE, stringsAsFactors = FALSE)

# # Verify data
# cat("Preview of Karyotype Data:\n")
# print(head(human_karyotype))
# cat("Preview of Gene Density Data:\n")
# print(head(gene_density))

# # Check if gene density is empty
# if (nrow(gene_density) == 0) {
#   stop("Error: Gene density data is empty. Cannot generate ideogram.")
# }

# # Specify output directory
# output_dir <- args[3]
# if (!dir.exists(output_dir)) {
#   dir.create(output_dir, recursive = TRUE)
# }

# # Output SVG file path
# svg_file <- file.path(output_dir, "chromosome.svg")

# # Generate ideogram (no fallback)
# tryCatch({
#   ideogram(
#     karyotype = human_karyotype,
#     overlaid = gene_density,
#     colorset1 = topo.colors(10),
#     colorset2 = terrain.colors(10),
#     output = svg_file
#   )
# }, error = function(e) {
#   stop("Error generating ideogram: ", e$message)
# })

# # Check if SVG was created
# if (!file.exists(svg_file)) {
#   stop("Error: SVG file not created.")
# }

# # Convert to PNG
# png_file <- file.path(output_dir, "chromosome.png")
# rsvg_png(svg_file, png_file)

# cat("Ideogram successfully generated:\n")
# cat("SVG:", svg_file, "\n")
# cat("PNG:", png_file, "\n")
# # Load required libraries
# library(RIdeogram)
# library(Cairo)
# library(rsvg)
# library(data.table)

# # Get command line arguments
# args <- commandArgs(trailingOnly = TRUE)

# # Check if the correct number of arguments are provided
# if (length(args) < 3) {
#   stop("Usage: Rscript generate_ideogram.R <karyotype_csv> <gene_density_csv> <output_dir>")
# }

# # Load data
# human_karyotype <- fread(args[1], sep = ",", header = TRUE, stringsAsFactors = FALSE)
# gene_density <- fread(args[2], sep = ",", header = TRUE, stringsAsFactors = FALSE)

# # Verify data
# cat("Preview of Karyotype Data:\n")
# print(head(human_karyotype))
# cat("Preview of Gene Density Data:\n")
# print(head(gene_density))

# # Specify output directory
# output_dir <- args[3]

# # Create output directory if it doesn't exist
# if (!dir.exists(output_dir)) {
#   dir.create(output_dir, recursive = TRUE)
# }

# # Generate ideogram
# svg_file <- file.path(output_dir, "chromosome.svg")
# ideogram(
#   karyotype = human_karyotype,
#   overlaid = gene_density,
#   colorset1 = topo.colors(10),
#   colorset2 = terrain.colors(10),
#   output = svg_file
# )

# # Check if SVG was created
# if (file.exists(svg_file)) {
#   cat("Ideogram SVG file generated successfully at:", svg_file, "\n")
# } else {
#   stop("Error: SVG file not created.")
# }
# Load required libraries
library(RIdeogram)
library(Cairo)
library(rsvg)
library(data.table)

# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check if the correct number of arguments are provided
if (length(args) < 3) {
  stop("Usage: Rscript generate_ideogram.R <karyotype_csv> <gene_density_csv> <output_dir>")
}

# Load data
human_karyotype <- fread(args[1], sep = ",", header = TRUE, stringsAsFactors = FALSE)
gene_density <- fread(args[2], sep = ",", header = TRUE, stringsAsFactors = FALSE)

# Verify data
cat("Preview of Karyotype Data:\n")
print(head(human_karyotype))
cat("Preview of Gene Density Data:\n")
print(head(gene_density))

# Check if gene density is empty
if (nrow(gene_density) == 0) {
  stop("Error: Gene density data is empty. Cannot generate ideogram. Please check the genelist first column should match with bedfile if not check the gff3")
}

# Specify output directory
output_dir <- args[3]
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Output SVG file path
svg_file <- file.path(output_dir, "chromosome.svg")

# Generate ideogram (no fallback)
tryCatch({
  ideogram(
    karyotype = human_karyotype,
    overlaid = gene_density,
    colorset1 = topo.colors(10),
    colorset2 = terrain.colors(10),
    output = svg_file
  )
}, error = function(e) {
  stop("Error generating ideogram: ", e$message)
})

# Check if SVG was created
if (!file.exists(svg_file)) {
  stop("Error: SVG file not created.")
}

# Convert to PNG
png_file <- file.path(output_dir, "chromosome.png")
rsvg_png(svg_file, png_file)

cat("Ideogram successfully generated:\n")
cat("SVG:", svg_file, "\n")
cat("PNG:", png_file, "\n")

