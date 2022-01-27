#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

if (!(length(args) %in% 3:4)) {
  cat("\nUsage:\n  unique-soundex.r names-in.txt derep-out.txt threads [code-length]\n\n")
  q("no")
}

library(parallel)
library(phonics)
infile  <- args[1]
outfile <- args[2]
threads <- as.numeric(args[3])
codelen <- if(length(args) == 4) as.integer(args[4]) else 15L
say <- function (...)
  message(paste("[", date(), "]", ..., "\n"), appendLF = FALSE)


say("- Reading names")
set.seed(3141516)
names <- read.table(infile, header = FALSE, as.is = TRUE, sep = "\t")[, 1]
names <- sample(names)

say("- Creating cluster")
cl <- makeCluster(threads)

say("- Calculating Refined Soundex codes")
soundex.code <- parSapply(
  cl, names,
  function(x, codelen) phonics::refinedSoundex(x, maxCodeLen = codelen),
  codelen = codelen
)

say("- Stopping cluster")
stopCluster(cl)

say("- Saving codes")
write.table(
  cbind(names, soundex.code), file = paste0(outfile, ".sdx"), quote = FALSE,
  col.names = FALSE, sep = "\t", row.names = FALSE
)

say("- Calculating phonetic uniqueness")
is.unique <- sapply(
  seq_along(soundex.code),
  function(x, soundex.code) !(soundex.code[x] %in% soundex.code[1:(x - 1)]),
  soundex.code = soundex.code
)
is.unique[1] <- TRUE

say("- Saving dereplicated name representatives")
write.table(
  names[is.unique], file = outfile, quote = FALSE,
  col.names = FALSE, sep = "\t", row.names = FALSE
)

