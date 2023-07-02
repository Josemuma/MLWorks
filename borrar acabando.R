library(pacman)
p_load(dplyr, readr, tm, stringdist, RecordLinkage, SimilarR)

# wates_21_txts <- read_rds(file = 'wates_21_txts')
# # Similarity ####
# # 3 ####
# # 1 vs New All
# results_03 <-
#     sapply(1:1, function(x) 
#       levenshteinSim(wates_21_txts[x,2],wates_21_txts[1:547,2]))
# # saveRDS(results_03, file = 'results_03')
# 
# 
# wates_21_txts[10,2]
# 
# wates_19_txts[10,2]
# 
# repeated_txts[5,2]
# repeated_txts[5,4]
# 
# stringsim(repeated_txts[5,2],repeated_txts[5,4]) #, method = 'cosine')
# stringsim(repeated_txts[5,2],repeated_txts[5,4], method = 'cosine')
# stringsim(repeated_txts[5,2],repeated_txts[5,4], method = 'jaccard')

# Comparison 1 ####
# lev_1to1 <- sapply(1:nrow(wates_match), function(x) 
#   levenshteinSim(repeated_txts[x,2],repeated_txts[x,4]))
# cosine_1to1 <- sapply(1:nrow(wates_match), function(x) 
#   stringsim(repeated_txts[x,2],repeated_txts[x,4], method = 'cosine'))
# jarow_1to1 <- sapply(1:nrow(wates_match), function(x) 
#   jarowinkler(repeated_txts[x,2],repeated_txts[x,4]))
# jaccard_1to1 <- sapply(1:nrow(wates_match), function(x) 
#   stringsim(repeated_txts[x,2],repeated_txts[x,4], method = 'jaccard'))
# bind_cols(cosine = cosine_1to1, jaccard = jaccard_1to1, jarow = jarow_1to1, lev = lev_1to1) %>% 
#   write.table(., file = 'Similarity_1v1.txt',
#               row.names = F, quote = F, sep = ',')




# Comparison 1 vs past ####
# # lev_1to1 <- 
#   sapply(1:nrow(wates_19_txts), function(x) 
#   levenshteinSim(wates_21_txts[6,2],wates_19_txts[x,2]))
# 
# sapply(1:nrow(wates_21_txts), function(x) 
#   levenshteinSim(wates_21_txts[6,2],wates_21_txts[x,2]))


wates_19_txts <-  read_rds(file = 'wates_19_txts')
wates_21_txts <- read_rds(file = 'wates_21_txts')

lev_1toNew <- sapply(1:nrow(wates_21_txts), function(y)
  sapply(1:nrow(wates_21_txts), function(x) 
    levenshteinSim(wates_21_txts[y,2],wates_21_txts[x,2])))

# saveRDS(lev_1toNew,file = 'lev_1toNew')






