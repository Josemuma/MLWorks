library(pacman)
p_load(cleanNLP, coreNLP, NLP,
       dplyr, readr, tm, stringdist, RecordLinkage, readxl)

# coreNLP::downloadCoreNLP()

library(coreNLP)
library(rJava)
initCoreNLP()

catInHat = c("the sun did not shine.", "it was too wet to play.",
             "so we sat in the house all that cold, cold, wet day.")
output = annotateString(catInHat)


library(cleanNLP)
library(dplyr)
library(magrittr)
library(ggplot2)
# cnlp_init_udpipe()
wates_21_txts <- readRDS('wates_21_txts')
wates_21_txts[1,]
annotation <- cnlp_annotate(input = wates_21_txts[1,2])
annotation


# cnlp_init_spacy('en_core_web_sm')

# cnlp_init_spacy('en_core_web_trf')

# spacy.load('en_core_web_sm')
cnlp_init_corenlp()

cnlp_init_spacy('en_core_web_md')
cnlp_init_spacy('en_core_web_lg')
# anno <- cnlp_annotate(input = wates_21_txts[367,2], verbose = F)
anno <- cnlp_annotate(input = wates_21_txts[sample(1:547,1),2], verbose = F) 

anno$token %>%
  group_by(doc_id, sid) %>%
  summarize(sent_len = n()) %$%
  quantile(sent_len, seq(0,1,0.1))

anno$token %>% filter(upos == "NOUN") %>%
  group_by(lemma) %>%
  summarize(count = n()) %>%
  top_n(n = 42, count) %>%
  arrange(desc(count)) %>%
  use_series(lemma)

anno$entity %>%
  filter(entity_type == "GPE") %>%
  # filter(entity_type == "ORG") %>%
  # filter(entity_type == "LOC") %>%
  # filter(entity_type == "PERSON") %>%
  # filter(entity_type == "TIME") %>%
  # filter(entity_type == "DATE") %>%
  group_by(entity) %>%
  summarize(count = n()) %>%
  top_n(n = 44, count) %>%
  arrange(desc(count)) %>%
  use_series(entity)





