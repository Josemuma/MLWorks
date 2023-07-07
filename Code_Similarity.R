#Load packages to use. 
library(pacman)
p_load(dplyr, readr, tm, stringdist, RecordLinkage, readxl)

# Read the name of the txt files to test for similarity
# Excel file needs to be store in the same folder as where the script is being ran. 
# Read the names of the companies that match 2021 and 2019
wates_match <- read_excel("Essex/Similarity_Results.xlsx",sheet = 'Matched_New_Old')

# Read the Wates adopters 2021
wates_21 <- read_excel("Essex/Similarity_Results.xlsx",sheet = 'Wates_21_547') %>%
  dplyr::select('Wates_21')

# Read the Wates adopters 2019
wates_19 <- read_excel("Essex/Similarity_Results.xlsx",sheet = 'Wates_19_338') %>%
  dplyr::select('Wates_19') %>% tidyr::drop_na()

# 2 Clean each of the txt files and store them in a matrix to compare them for the 
# three required tests.
# The TXTs have to be in the same folder as this script or a subfolder works too. 

# Matched Files ####
# repeated_txts <- data.frame()
# for(i in 1:nrow(wates_match)){
#   x <- wates_match[i,1]
#   x_txt <- read_file(paste('Essex/20_21_Wates_readable_texts_547/', x, sep = '')) %>%
#     gsub("\\n"," ", .) %>% # Removes "\n" which means a new line
#     gsub("Highlight [[]page [[:digit:]]+[]]:"," ", .) %>% # Removes the line "Highlight [page ##]:"
#     removeWords(., words = stopwords('english')) %>% # Remove stopwords from an English dictionary
#     gsub("[[:punct:]]", " ", .) %>%  # Remove punctuations
#     gsub("[[:digit:]]+"," ", .) # Remove numbers/digits
# 
#   y <- wates_match[i,2]
#   y_txt <- read_file(paste('Essex/19_20_Wates_338 Txt files of readable reports/', y, sep = '')) %>%
#     gsub("\\n"," ", .) %>% # Removes "\n" which means a new line
#     gsub("\\r"," ", .) %>% # Removes "\n" which means a new line also
#     gsub("Highlight [[]page [[:digit:]]+[]]:"," ", .) %>% # Removes the line "Highlight [page ##]:"
#     removeWords(., words = stopwords('english')) %>% # Remove stopwords from an English dictionary
#     gsub("[[:punct:]]", " ", .) %>%  # Remove punctuations
#     gsub("[[:digit:]]+"," ", .) # Remove numbers/digits
# 
#   repeated_txts[i,1] <- wates_match[i,1] # Store file name in column 1
#   repeated_txts[i,2] <- x_txt # Store text in column 2
#   repeated_txts[i,3] <- wates_match[i,2] # Store file name in column 3
#   repeated_txts[i,4] <- y_txt # Store text in column 4
# }
# #saveRDS(repeated_txts, file = 'repeated_txts')
# With the line below there is no need to re-run the previous step, just load the matrix
repeated_txts <- read_rds(file = 'repeated_txts')

# WATES 2021 ####
# repeated_txts <- data.frame()
# It looks through each file name for its corresponding text and stores the name and the text, in each column
# wates_21_txts <- data.frame()
# for (i in 1:nrow(wates_21)) {
# # for (i in 1:11) {
#   x <- wates_21[i,1]
#   x_txt <- read_file(paste('Essex/20_21_Wates_readable_texts_547/', x, sep = '')) %>%
#     gsub("\\n"," ", .) %>% # Removes "\n" which means a new line
#     gsub("Highlight [[]page [[:digit:]]+[]]:"," ", .) %>% # Removes the line "Highlight [page ##]:"
#     removeWords(., words = stopwords('english')) %>% # Remove stopwords from an English dictionary
#     gsub("[[:punct:]]", " ", .) %>%  # Remove punctuations
#     gsub("[[:digit:]]+"," ", .) # Remove numbers/digits 
#   wates_21_txts[i,1] <- x # Store file name in column 1
#   wates_21_txts[i,2] <- x_txt # Store text in column 2
# }
# #saveRDS(wates_21_txts, file = 'wates_21_txts') # Save the matrix
# With the line below there is no need to re-run the previous step, just load the matrix
wates_21_txts <- read_rds(file = 'wates_21_txts') 

# WATES 2019 ####
# wates_19_txts <- data.frame()
# for (i in 1:nrow(wates_19)) {
#   y <- wates_19[i,1]
#   y_txt <- read_file(paste('Essex/19_20_Wates_338 Txt files of readable reports/', y, sep = '')) %>%
#     gsub("\\n"," ", .) %>% # Removes "\n" which means a new line
#     gsub("\\r"," ", .) %>% # Removes "\n" which means a new line also
#     gsub("Highlight [[]page [[:digit:]]+[]]:"," ", .) %>% # Removes the line "Highlight [page ##]:"
#     removeWords(., words = stopwords('english')) %>% # Remove stopwords from an English dictionary
#     gsub("[[:punct:]]", " ", .) %>%  # Remove punctuations
#     gsub("[[:digit:]]+"," ", .) # Remove numbers/digits 
#   wates_19_txts[i,1] <- y  # Store file name in column 1
#   wates_19_txts[i,2] <- y_txt # Store text in column 2
# }
# #saveRDS(wates_19_txts, file = 'wates_19_txts')
# With the line below there is no need to re-run the previous step, just load the matrix
wates_19_txts <-  read_rds(file = 'wates_19_txts')




# Similarity ####
# 1 to 1 ####
# The similarity test is ran for two different methods
## JW ####
jw_1to1 <- sapply(1:nrow(wates_match), function(x)
  jarowinkler(repeated_txts[x,2],repeated_txts[x,4])) %>%
  # stringsim(repeated_txts[x,2],repeated_txts[x,4], method = "jw")) %>% # alternative pacakge same results
  cbind(Company_2021 = repeated_txts$Wates_21, Similarity_JW = .) # Bind name of Wates 2021 TXT file
# Then save it as a TXT
write.table(jw_1to1, file = 'jw_1to1.txt', quote = F, row.names = F, sep = ',')

# Lev ####
lev_1to1 <- sapply(1:nrow(wates_match), function(x)
  levenshteinSim(repeated_txts[x,2],repeated_txts[x,4])) %>%
  # stringsim(repeated_txts[x,2],repeated_txts[x,4], method = "lv")) %>% # alternative pacakge same results
  cbind(Company_2021 = repeated_txts$Wates_21, Similarity_Lev = .) # Bind name of Wates 2021 TXT file
# Then save it as a TXT
write.table(lev_1to1, file = 'lev_1to1.txt', quote = F, row.names = F, sep = ',')


# 1 to Past ####
# The similarity test is ran for two different methods
## JW ####
jw_1toPast <- sapply(1:nrow(wates_21_txts), function(y)
  sapply(1:nrow(wates_19_txts), function(x) 
    jarowinkler(wates_21_txts[y,2],wates_19_txts[x,2])))
    # stringsim(wates_21_txts[y,2],wates_19_txts[x,2], method = "jw"))) %>% # alternative pacakge same results
saveRDS(jw_1toPast, 'jw_1toPast')
# Then save it as a TXT
bind_cols(
  wates_21 %>% tibble(.) %>% 
    add_row(Wates_21 =  "Companies",.before = 1),
  t(bind_cols(wates_19,(jw_1toPast)%>% tibble(.))) %>% 
    tibble(.)) %>% 
  write.table(., file = 'jw_1toPast.txt', quote = F, 
              row.names = F, col.names = F, sep = '|')
## Lev ####
# This method takes up to 25 hours to run 
lev_1toPast <- sapply(1:nrow(wates_21_txts), function(y)
  sapply(1:nrow(wates_19_txts), function(x) 
    levenshteinSim(wates_21_txts[y,2],wates_19_txts[x,2])))
    # stringsim(wates_21_txts[y,2],wates_19_txts[x,2], method = "lv"))) %>% # alternative pacakge same results
saveRDS(lev_1toPast, 'lev_1toPast')
# Then save it as a TXT
bind_cols(
  wates_21 %>% tibble(.) %>% 
    add_row(Wates_21 =  "Companies",.before = 1),
  t(bind_cols(wates_19,(lev_1toPast)%>% tibble(.))) %>% 
    tibble(.)) %>% 
  write.table(., file = 'lev_1toPast.txt', quote = F, 
              row.names = F, col.names = F, sep = '|')

# 1 to New ####
# The similarity test is ran for two different methods
## JW ####
jw_1toNew <- sapply(1:nrow(wates_21_txts), function(y)
  sapply(1:nrow(wates_21_txts), function(x)
    jarowinkler(wates_21_txts[y,2],wates_21_txts[x,2])))
    # stringsim(wates_21_txts[y,2],wates_21_txts[x,2], method = "jw"))) %>% # alternative pacakge same results
saveRDS(jw_1toNew, 'jw_1toNew')
# Then save it as a TXT
bind_cols(
  wates_21 %>% tibble(.) %>% 
    add_row(Wates_21 =  "Companies",.before = 1),
  t(bind_cols(wates_21,(jw_1toNew)%>% tibble(.))) %>% 
    tibble(.)) %>% 
  write.table(., file = 'jw_1toNew.txt', quote = F, 
              row.names = F, col.names = F, sep = '|')

## Lev ####
# This method takes up to 36 hours to run 
lev_1toNew <- sapply(1:nrow(wates_21_txts), function(y)
  sapply(1:nrow(wates_21_txts), function(x) 
    levenshteinSim(wates_21_txts[y,2],wates_21_txts[x,2])))
    # stringsim(wates_21_txts[y,2],wates_21_txts[x,2], method = "lv"))) %>% # alternative pacakge same results
saveRDS(lev_1toNew, 'lev_1toNew')
# Then save it as a TXT
bind_cols(
  wates_21 %>% tibble(.) %>% 
    add_row(Wates_21 =  "Companies",.before = 1),
  t(bind_cols(wates_21,(lev_1toNew)%>% tibble(.))) %>% 
    tibble(.)) %>% 
  write.table(., file = 'lev_1toNew.txt', quote = F, 
              row.names = F, col.names = F, sep = '|')























