# # # Load required library
# # library(GenomicRanges)
# # library(stats4)

# # # Function to replicate bedtools makewindows functionality
# # make_windows <- function(genome_file, window_size, output_file) {
# #   # Step 1: Read the genome size file
# #   genome <- read.table(genome_file, header = FALSE, stringsAsFactors = FALSE)
# #   colnames(genome) <- c("chrom", "size")
  
# #   # Step 2: Create windows for each chromosome
# #   windows_list <- list()
# #   for (i in 1:nrow(genome)) {
# #     chrom <- genome$chrom[i]
# #     size <- genome$size[i]
# #     starts <- seq(0, size - window_size, by = window_size)
# #     ends <- starts + window_size
# #     ends <- pmin(ends, size)  # Ensure windows don't exceed chromosome size
# #     if (ends[length(ends)] < size) {  # Add a final window for the leftover region
# #       starts <- c(starts, ends[length(ends)])
# #       ends <- c(ends, size)
# #     }
# #     windows_list[[i]] <- data.frame(chrom = chrom, start = starts, end = ends)
# #   }
  
# #   # Step 3: Combine all windows and write to output file
# #   windows_df <- do.call(rbind, windows_list)
# #   tryCatch({
# #     write.table(windows_df, output_file, quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
# #     cat("Windows written to:", output_file, "\n")
# #   }, error = function(e) {
# #     cat("Error writing file:", e$message, "\n")
# #     stop(e)
# #   })
# # }

# # # Main execution
# # args <- commandArgs(trailingOnly = TRUE)
# # if (length(args) != 3) {
# #   stop("Usage: Rscript make_windows.R <genome_file> <window_size> <output_file>")
# # }

# # genome_file <- args[1]
# # window_size <- as.numeric(args[2])
# # output_file <- args[3]

# # # Run the make_windows function
# # make_windows(genome_file, window_size, output_file)

# # Load required library
# library(GenomicRanges)
# library(stats4)

# # Function to replicate bedtools makewindows functionality
# make_windows <- function(genome_file, window_size, output_file) {
#   # Step 1: Read the genome size file
#   genome <- read.table(genome_file, header = FALSE, stringsAsFactors = FALSE)
#   colnames(genome) <- c("chrom", "size")
  
#   # Step 2: Create windows for each chromosome
#   windows_list <- list()
#   for (i in 1:nrow(genome)) {
#     chrom <- genome$chrom[i]
#     size <- genome$size[i]
    
#     # 🚫 Add error check for window size
#     if (window_size > size) {
#       stop(paste0("Error: Window size (", window_size, 
#                   ") is larger than the size of chromosome ", chrom, 
#                   " (", size, "). Cannot create any windows."))
#     }
    
#     starts <- seq(0, size - window_size, by = window_size)
#     ends <- starts + window_size
#     ends <- pmin(ends, size)  # Ensure windows don't exceed chromosome size
    
#     if (ends[length(ends)] < size) {  # Add a final window for the leftover region
#       starts <- c(starts, ends[length(ends)])
#       ends <- c(ends, size)
#     }
    
#     windows_list[[i]] <- data.frame(chrom = chrom, start = starts, end = ends)
#   }
  
#   # Step 3: Combine all windows and write to output file
#   windows_df <- do.call(rbind, windows_list)
  
#   tryCatch({
#     write.table(windows_df, output_file, quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
#     cat("Windows written to:", output_file, "\n")
#   }, error = function(e) {
#     cat("Error writing file:", e$message, "\n")
#     stop(e)
#   })
# }

# # Main execution
# args <- commandArgs(trailingOnly = TRUE)
# if (length(args) != 3) {
#   stop("Usage: Rscript make_windows.R <genome_file> <window_size> <output_file>")
# }

# genome_file <- args[1]
# window_size <- as.numeric(args[2])
# output_file <- args[3]

# # Run the make_windows function
# make_windows(genome_file, window_size, output_file)

# Load required libraries
library(GenomicRanges)
library(stats4)

# Function to replicate bedtools makewindows functionality
make_windows <- function(genome_file, window_size, output_file) {
  # Step 1: Read the genome size file
  genome <- read.table(genome_file, header = FALSE, stringsAsFactors = FALSE)
  colnames(genome) <- c("chrom", "size")
  
  # Step 2: Create windows for each chromosome
  windows_list <- list()
  for (i in 1:nrow(genome)) {
    chrom <- genome$chrom[i]
    size <- genome$size[i]
    
    # Check: Window size must not exceed chromosome size
    if (window_size > size) {
      stop(paste0("Error: Window size (", window_size, 
                  ") is larger than chromosome ", chrom, 
                  " size (", size, "). Cannot create any windows."))
    }
    
    starts <- seq(0, size - window_size, by = window_size)
    ends <- starts + window_size
    ends <- pmin(ends, size)  # Ensure windows do not exceed chromosome size
    
    if (ends[length(ends)] < size) {
      starts <- c(starts, ends[length(ends)])
      ends <- c(ends, size)
    }
    
    windows_list[[i]] <- data.frame(chrom = chrom, start = starts, end = ends)
  }

  # Step 3: Combine all windows
  windows_df <- do.call(rbind, windows_list)

  # Step 4: Write to output file
  tryCatch({
    write.table(windows_df, output_file, quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)
  }, error = function(e) {
    stop("Error writing output file: ", e$message)
  })

  # Confirm file was written
  if (!file.exists(output_file)) {
    stop("Output file was not created: ", output_file)
  }

  cat("Windows written to:", output_file, "\n")
}

# Main script execution
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop("Usage: Rscript make_windows.R <genome_file> <window_size> <output_file>")
}

genome_file <- args[1]
window_size <- as.numeric(args[2])
output_file <- args[3]

# Run the function
make_windows(genome_file, window_size, output_file)
