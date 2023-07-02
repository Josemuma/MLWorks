library(pacman)
p_load(dplyr, readr, tm, stringdist, RecordLinkage, readxl)
# list.files('Essex/20_21_Wates_readable texts_547/') %>% 
#   tibble(.) %>% 
#   write.table(., file = '21_wates.txt', quote = F, row.names = F)
# 
# 
# list.files('Essex/19_20_Wates_338 Txt files of readable reports/') %>% 
#   tibble(.) %>% 
#   write.table(., file = '19_wates.txt', quote = F, row.names = 
# Load ####
## Names ####
wates_match <- read_excel("Essex/Matching_Txts.xlsx",sheet = 'Match_21_19')

wates_21 <- read_excel("Essex/Matching_Txts.xlsx",sheet = 'All_Companies') %>%
  dplyr::select('Wates_21')

wates_19 <- read_excel("Essex/Matching_Txts.xlsx",sheet = 'All_Companies') %>%
  dplyr::select('Wates_19') %>% tidyr::drop_na()

levenshteinSim(repeated_txts[5,2],repeated_txts[5,4])
jarowinkler(repeated_txts[5,2],repeated_txts[5,4])


## Texts ####
repeated_txts <- read_rds(file = 'repeated_txts')
wates_19_txts <-  read_rds(file = 'wates_19_txts')
wates_21_txts <- read_rds(file = 'wates_21_txts')

# JW ####
## 1 vs 1 ####
# jw_1to1 <- sapply(1:nrow(wates_match), function(x)
  sapply(1:1, function(x) 
    jarowinkler(repeated_txts[x,2],repeated_txts[x,4]))
)

## 1 vs P ####
jw_1toPast <- sapply(1:nrow(wates_21_txts), function(y)
  sapply(1:nrow(wates_19_txts), function(x) 
    jarowinkler(wates_21_txts[y,2],wates_19_txts[x,2])))

## 1 vs N####
jw_1toNew <- sapply(1:nrow(wates_21_txts), function(y)
  sapply(1:nrow(wates_21_txts), function(x)
    jarowinkler(wates_21_txts[y,2],wates_21_txts[x,2])))






# Lev ####
## 1 vs 1 ####
# lev_1to1 <- sapply(1:nrow(wates_match), function(x)
sapply(1:nrow(wates_match), function(x)
  levenshteinSim(repeated_txts[x,2],repeated_txts[x,4]))

## 1 vs P ####
lev_1toPast <- sapply(1:nrow(wates_21_txts), function(y)
  sapply(1:nrow(wates_19_txts), function(x) 
    levenshteinSim(wates_21_txts[y,2],wates_19_txts[x,2])))
# saveRDS(lev_1toPast,file = 'lev_1toPast')


## 1 vs N####
lev_1toNew <- sapply(1:nrow(wates_21_txts), function(y)
  sapply(1:nrow(wates_21_txts), function(x) 
    levenshteinSim(wates_21_txts[y,2],wates_21_txts[x,2])))
# saveRDS(lev_1toNew,file = 'lev_1toNew')










# Matched ####
# repeated_txts <- data.frame()
# for(i in 1:nrow(wates_match)){
#   x <- wates_match[i,1]
#   x_txt <- read_file(paste('Essex/20_21_Wates_readable_texts_547/', x, sep = '')) %>%
#     gsub("\\n"," ", .) %>%
#     gsub("Highlight [[]page [[:digit:]]+[]]:"," ", .)  %>%
#     removeWords(., words = stopwords('english')) %>%
#     gsub("[[:punct:]]", " ", .) %>% 
#     gsub("[[:digit:]]+"," ", .) 
#   
#   y <- wates_match[i,2]
#   y_txt <- read_file(paste('Essex/19_20_Wates_338 Txt files of readable reports/', y, sep = '')) %>%
#     gsub("\\n"," ", .) %>%
#     gsub("\\r"," ", .) %>%
#     gsub("Highlight [[]page [[:digit:]]+[]]:"," ", .)  %>%
#     removeWords(., words = stopwords('english')) %>%
#     gsub("[[:punct:]]", " ", .) %>% 
#     gsub("[[:digit:]]+"," ", .) 
#   
#   repeated_txts[i,1] <- wates_match[i,1]
#   repeated_txts[i,2] <- x_txt
#   repeated_txts[i,3] <- wates_match[i,2]
#   repeated_txts[i,4] <- y_txt
# }
# # saveRDS(repeated_txts, file = 'repeated_txts')
# # repeated_txts <- read_rds(file = 'repeated_txts')

## WATES 21 ####
# wates_21_txts <- data.frame()
# for (i in 1:nrow(wates_21)) {
# # for (i in 1:11) {
#   x <- wates_21[i,1]
#   x_txt <- read_file(paste('Essex/20_21_Wates_readable_texts_547/', x, sep = '')) %>%
#     gsub("\\n"," ", .) %>%
#     gsub("Highlight [[]page [[:digit:]]+[]]:"," ", .)  %>%
#     removeWords(., words = stopwords('english')) %>%
#     gsub("[[:punct:]]", " ", .) %>% 
#     gsub("[[:digit:]]+"," ", .) 
#   wates_21_txts[i,1] <- x
#   wates_21_txts[i,2] <- x_txt
# }
# # saveRDS(wates_21_txts, file = 'wates_21_txts')
# # wates_21_txts <- read_rds(file = 'wates_21_txts')

## WATES 19 ####
# wates_19_txts <- data.frame()
# for (i in 1:nrow(wates_19)) {
#   y <- wates_19[i,1]
#   y_txt <- read_file(paste('Essex/19_20_Wates_338 Txt files of readable reports/', y, sep = '')) %>%
#     gsub("\\n"," ", .) %>%
#     gsub("\\r"," ", .) %>%
#     gsub("Highlight [[]page [[:digit:]]+[]]:"," ", .)  %>%
#     removeWords(., words = stopwords('english')) %>%
#     gsub("[[:punct:]]", " ", .) %>% 
#     gsub("[[:digit:]]+"," ", .) 
#   wates_19_txts[i,1] <- y
#   wates_19_txts[i,2] <- y_txt
# }
# # # saveRDS(wates_19_txts, file = 'wates_19_txts')
# # wates_19_txts <-  read_rds(file = 'wates_19_txts')