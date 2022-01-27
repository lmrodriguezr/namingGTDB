#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 3) {
  cat("\nUsage:\n  min-levenshtein.r names-in.txt minlev-out.tsv threads\n\n")
  q("no")
}

library(parallel)
infile  <- args[1]
outfile <- args[2]
threads <- as.numeric(args[3])
say <- function (...)
  message(paste("[", date(), "]", ..., "\n"), appendLF = FALSE)


say("- Reading names")
set.seed(3141516)
names <- read.table(infile, header = FALSE, as.is = TRUE, sep = "\t")[, 1]
names <- sample(names)

say("- Creating cluster")
cl <- makeCluster(threads)

say("- Calculating minimum Levenshtein distance")
min.dist <- parSapply(
  cl, seq_along(names),
  function(x, names) min(adist(names[x], names[1:(x - 1)], ignore.case = TRUE)),
  names = names
)
min.dist[1] <- Inf

say("- Stopping cluster")
stopCluster(cl)

say("- Saving minimum distances from name representatives")
write.table(
  cbind(names, min.dist), file = outfile, quote = FALSE, sep = "\t",
  col.names = FALSE, row.names = FALSE
)

