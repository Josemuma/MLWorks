library(readr)
test <- file('~/Desktop/Essex_2/TXTs/ADVISORY INSURANCE BROKERS LIMITED_04043759.txt', 
             open = 'r')
test

x <- read_file("~/Desktop/Essex_2/TXTs/ADVISORY INSURANCE BROKERS LIMITED_04043759.txt")
x <- read_file("~/Desktop/Essex_2/TXTs/AGEAS INSURANCE LIMITED_00354568.txt")
x
# x <- read.delim("~/Desktop/Essex_2/TXTs/ADVISORY INSURANCE BROKERS LIMITED_04043759.txt")
# x
# x_new <- 
  # gsub("(\n)(Highlight )([[])(page )([[:digit:]])([[:digit:]])([]])(:)"," ", x,fixed = T)
gsub("Highlight [page )"," ", x,fixed = T)
x_new
write.table(x_new,
            file = "tset.txt",
            row.names = F,
            col.names = F,
            eol = "\n",
            # sep = '", "',
            quote = F)

# ^ Start of pattern.
# () Group (or token).
# \w* One or more occurrences of word character more than 1 times.
# .* one or more occurrences of any character except new line \n.
# $ end of pattern.
# \1 Returns group from regexp
