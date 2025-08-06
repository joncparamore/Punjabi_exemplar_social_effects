


####------------IMPORTS-----------####


library(dplyr)
library(tidyr)
library(stringr)
library(ggplot2)

####-----------LOAD DATAFRAMES---------------####

#------------Combine with Punjabi Corpus (to get Lexical Frequency)-----------#

df1_tokens <- read.csv("/Users/steffikim/Downloads/tokens_shahmukhi_ipa.csv")
df2_corpus <- read.csv("/Users/steffikim/Downloads/Punjabi_Corpus.csv")

df3_combined <- left_join(df1_tokens, df2_corpus, by = c("Shahmukhi" = "Word"))


#Remove repeated rows, reset the row numbers from 1 to 66
df3_combined <- unique(df3_combined)
rownames(df3_combined) <- NULL


#------------Combine with Speaker Info-----------#


df4_all_speaker_info <- read.csv("/Users/steffikim/Downloads/experiment_tokens_shahmukhi_translation_ipa_gloss.xlsx - Sheet1.csv")


#Only select the relevant data columns
df4_speaker_info <- df4_all_speaker_info %>% select("Panjabi", "IPA","vowel", "onset", "coda", "Voice")


#Fix some spelling inconsistencies that get lost in translation
df4_speaker_info$IPA <- str_replace_all(df4_speaker_info$IPA,"a","ɑ")
df4_speaker_info$IPA <- str_replace_all(df4_speaker_info$IPA,"v","ʋ")

df3_combined <- inner_join(df3_combined, df4_speaker_info, by = "IPA")


#missing_entries_check <- anti_join(df4_speaker_info, df3_combined, by = "IPA")

#Clean up work space
rm(df1_tokens,df2_corpus,df4_all_speaker_info, df4_speaker_info)



#------------Combine with Experimental Data Audio Measures ------------#


df5_audio_measurements <- read.csv("/Users/steffikim/Downloads/MR0_pan_2025_exemplar_measurements.csv")


#Clean column values, convert certain columns to numeric
df5_audio_measurements <- df5_audio_measurements %>% 
  mutate(across(c("F0_1","F0_2","F0_3","F0_4","F0_5","F0_6","F0_7","F0_8","F0_9","F0_10"),
                ~ as.numeric(str_replace_all(.x," Hz","")))) %>%
  mutate(across(c("Duration", "MeanF0", "MeanIntensity", "MaxIntensity", "F1", "F2", "F3", "Spectral_Tilt"),
                ~ as.numeric(.x))) 


#Fix some spelling inconsistencies that get lost in translation
df3_combined$IPA[df3_combined$IPA =="dʒõõk "] <- "dʒõõk"

df5_audio_measurements$word[df5_audio_measurements$word =="põõtʃ"] <- "põõtʃ"
df5_audio_measurements$word[df5_audio_measurements$word =="dʒõõ"] <- "dʒõõ"
df5_audio_measurements$word[df5_audio_measurements$word =="dʒõõk"] <- "dʒõõk"
df5_audio_measurements$word[df5_audio_measurements$word =="pĩĩg"] <-"pĩĩg"


#missing_entries_check_2 <- anti_join(df5_audio_measurements, df3_combined, by =  c("word" = "IPA"))


df3_combined <- left_join(df3_combined, df5_audio_measurements, by =  c("IPA" = "word"))


df3_combined <- df3_combined %>% separate_wider_delim(filename,delim="_",names=c("Delete1", "Delete2", "speaker", "Phase", "Delete3"), too_many="merge")
df3_combined <- df3_combined %>% select(-c("Delete1", "Delete2", "Delete3", "Panjabi"))

rm(df5_audio_measurements) #No longer needed, can clean up space

#------------Transform to vertical form-----------#


df3_combined_long <- df3_combined %>%
  pivot_longer(
    cols = starts_with("F0_"),
    names_to = "step",
    values_to = "F0"
  ) %>%
  mutate(
    step=as.integer(gsub("F0_", "", step)) 
      )

df3_combined_long$Phase <- as.factor(df3_combined_long$Phase)

df3_combined_long <- df3_combined_long %>% mutate(condition = paste(Phase,Voice,sep = "_"))


#------------Add in the Exemplar Voices-----------#

#Rename certain columns for consistency purposes before the data frames are combined
df3_combined_long <- df3_combined_long %>% rename("segment"="vowel", "voice" = "Voice", "word" = "IPA")

df7_exemplar_measures <- read.csv("/Users/steffikim/Downloads/voices_pan_2025_exemplar_measurements.csv")
df7_exemplar_measures <- df7_exemplar_measures %>% mutate(Phase = "exemplar")


#Clean Data and transform to correct column types i.e. numeric, etc.

df7_exemplar_measures <- df7_exemplar_measures %>% 
  mutate(across(c("F0_1","F0_2","F0_3","F0_4","F0_5","F0_6","F0_7","F0_8","F0_9","F0_10"),
                ~ as.numeric(str_replace_all(.x," Hz","")))) %>%
  mutate(across(c("Duration", "MeanF0", "MeanIntensity", "MaxIntensity", "F1", "F2", "F3", "Spectral_Tilt"),
                ~ as.numeric(.x))) 


df7_exemplar_measures <- df7_exemplar_measures %>% mutate(condition = paste(Phase,voice,sep = "_"))



#Transform to vertical form


df7_exemplar_measures <- df7_exemplar_measures %>%
  pivot_longer(
    cols = starts_with("F0_"),
    names_to = "step",
    values_to = "F0"
  ) %>%
  mutate(
    step=as.integer(gsub("F0_", "", step)) 
  )


#Combine the Exemplar Data with the large data frame using bind_rows

df3_combined_long$Phase <- as.factor(df3_combined_long$Phase)
df3_combined_long <- bind_rows(df3_combined_long, df7_exemplar_measures)



####---------------------VISUALIZE DATA----------------------####

#Create theme object that stores the consistent plot setings

my_theme <- list(theme(
  plot.title = element_text(face = "bold", hjust = 0.5),
  axis.title = element_text(face = "bold", size = 10),
  axis.text = element_text(face = "bold", size = 10),
  legend.title = element_text(face = "bold", size = 12, hjust = 0.5),
  legend.text = element_text(face = "bold", size = 10),
  legend.key = element_rect(fill = "white"),
  plot.background = element_rect(fill = "white", color = "white"),
  panel.background = element_rect(fill = "white"),
  panel.grid.major = element_line(color = "lightgrey"),
  panel.grid.minor = element_line(color = "lightgrey"),
  legend.position = "right"
),
  scale_x_continuous(
    breaks = c(1, 4, 7, 10),  # Specify the positions of the labels
    labels = c(1, 4, 7, 10)  # Use custom labels on x axis
  ) )


####-------------All Info Plot----------------####



p_all_info <- df3_combined_long %>% ggplot() +
  geom_smooth(mapping = aes(x=step,y=F0,color= condition, linetype = condition),
              linewidth=1,se=F, span=0.5) +
  
  labs(
    title = "All Information",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase", linetype = "Phase"
  ) +
  scale_color_manual(
    values = c(
      
      "baseline_AK1" = "#da216d",
      "baseline_AT0" = "#f29813",
      "baseline_None" = "#ffc002",
      "exemplar_AK1" = "#8F639B",
      "exemplar_AT0" = "#012060",
      "postproductions_AK1" = "#13a5dc",
      "postproductions_AT0" = "#93c02d",
      "postproductions_None" = "#007988",
      "shadow_AK1" = "#006aad",
      "shadow_AT0" = "#2F7B33"
      
    ),
    labels = c(
      "Baseline of LP Words",
      "Baseline of HP Words",
      "Baseline of Non-Shadowed Words",
      "Low Prestige Voice",
      "High Prestige Voice",
      "Postproductions of LP Words",
      "Postproductions of HP Words",
      "Postproductions of Non-Shadowed Words",
      "Shadow of LP Words",
      "Shadow of HP Words"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "baseline_AK1" = "solid",
      "baseline_AT0" = "dashed",
      "baseline_None" = "longdash",
      "exemplar_AK1" = "twodash",
      "exemplar_AT0" = "dotdash",
      "postproductions_AK1" = "solid",
      "postproductions_AT0" = "dashed",
      "postproductions_None" = "longdash",
      "shadow_AK1" = "twodash",
      "shadow_AT0" = "dotdash"
      ),
    labels = c(
      "Baseline of LP Words",
      "Baseline of HP Words",
      "Baseline of Non-Shadowed Words",
      "Low Prestige Voice",
      "High Prestige Voice",
      "Postproductions of LP Words",
      "Postproductions of HP Words",
      "Postproductions of Non-Shadowed Words",
      "Shadow of LP Words",
      "Shadow of HP Words"
    )
  ) + my_theme


print(p_all_info)

####-----------------Basic Phase Plots ---------------------####


#Create a new column called "phase_label" for the purpose of making these next plots. This allows plotting with ggplot to be intuitive and avoids confusion with multiple factors/making the legends messy
df3_combined_long <- df3_combined_long %>%
  mutate(phase_label = case_when(
    Phase == "baseline" ~ "Baseline",
    condition == "exemplar_AT0" ~ "High Prestige Voice",
    condition == "exemplar_AK1" ~ "Low Prestige Voice",
    condition == "shadow_AT0" ~ "Participant Shadow of HP",
    condition == "shadow_AK1" ~ "Participant Shadow of LP",
    Phase == "postproductions" ~ "Postproduction",
  ))  %>%  
  mutate(phase_label = factor(phase_label, levels = c("Baseline", "High Prestige Voice", "Low Prestige Voice", "Participant Shadow of HP", "Participant Shadow of LP", "Postproduction")))




p_phases <- ggplot() + 
  geom_smooth(data = df3_combined_long %>% filter(Phase == "baseline"|Phase == "exemplar"|Phase == "postproductions" ), mapping = aes(x=step,y=F0,color= phase_label, linetype = phase_label),
                            linewidth=1,se=T, span=0.5) + 
  
  labs(
    title = "F0 Contours of Baseline, Exemplars, & Postproduction",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase", linetype = "Phase"
  ) +
  scale_color_manual(
    values = c(
      "Baseline" = "#da216d",
      "High Prestige Voice" = "#f29813",
      "Low Prestige Voice" = "#13a5dc",
      "Postproduction" = "#012060"
    ),
    labels = c(
      "Baseline",
      "High Prestige Voice",
      "Low Prestige Voice",
      "Postproduction"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "Baseline" = "solid",
      "High Prestige Voice" = "dotdash",
      "Low Prestige Voice" = "dashed",
      "Postproduction" = "longdash"
    ),
    labels = c(
      "Baseline",
      "High Prestige Voice",
      "Low Prestige Voice",
      "Postproduction"
    )
  ) + my_theme
                

print(p_phases)



#Make a plot of just the two exemplar voices

p_exemplar_only <- ggplot() + 
  geom_smooth(data = df3_combined_long%>% filter(Phase == "exemplar"), mapping = aes(x=step,y=F0,color= phase_label, linetype = phase_label),
              linewidth=1,se=F, span=0.5) +
  labs(
    title = "F0 Contours of Exemplar Voices",
    x = "Timestep", y = "F0 (Hz)",
    color = "Category", linetype = "Category"
  ) + scale_color_manual(
    values = c(
      "High Prestige Voice" = "#13a5dc",
      "Low Prestige Voice" = "#f29813"
    ),
    labels = c(
      "High Prestige Voice",
      "Low Prestige Voice"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "High Prestige Voice" = "dashed",
      "Low Prestige Voice" = "solid"
    ),
    labels = c(
      "High Prestige Voice",
      "Low Prestige Voice"
    ))+ my_theme


print(p_exemplar_only)



#Make a plot showing the two exemplar voices and two lines for their respective shadows

p_exemplar_and_shadow <- ggplot() + 
  geom_smooth(data = df3_combined_long %>% filter(Phase == "exemplar"|Phase == "shadow"), mapping = aes(x=step,y=F0,color= phase_label, linetype = phase_label),
              linewidth=1,se=F, span=0.5) + 
  labs(
    title = "F0 Contours of Exemplars and Shadowing Phase",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase", linetype = "Phase"
  )   +scale_color_manual(
    values = c(
      "High Prestige Voice" ="#13a5dc",
      "Low Prestige Voice" = "#f29813",
      "Participant Shadow of HP" = "#93c02d",
      "Participant Shadow of LP" = "#007988"
    ),
    labels = c(
      "High Prestige Voice",
      "Low Prestige Voice",
      "Participant Shadow of HP",
      "Participant Shadow of LP"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "High Prestige Voice" = "solid",
      "Low Prestige Voice" = "solid",
      "Participant Shadow of HP" = "dashed",
      "Participant Shadow of LP" = "dashed"
    ),
    labels = c(
      "High Prestige Voice",
      "Low Prestige Voice",
      "Participant Shadow of HP",
      "Participant Shadow of LP"
    ))+ 
  my_theme


print(p_exemplar_and_shadow )




#Basic plot of just the baseline and postproduction phase

p_baseline_postproduction_only<- ggplot() + 
  geom_smooth(data = df3_combined_long %>% filter(Phase == "baseline" | Phase == "postproductions"), mapping = aes(x=step,y=F0,color= Phase, linetype = Phase),
              linewidth=1,se=T, span=0.5)  +
  labs(
    title = "F0 Contours of Overall Baseline and Postproduction",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase", linetype = "Phase"
  ) + scale_color_manual(
    values = c(
      "baseline" = "#da216d",
      "postproductions" = "#012060"
    ),
    labels = c(
      "Baseline",
      "Postproduction"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "baseline" = "solid",
      "postproductions" = "dashed"
    ),
    labels = c(
      "Baseline",
      "Postproduction"
    )
  ) + my_theme
print(p_baseline_postproduction_only)



#Postproductions Only

#Plot of just the postproduction words categorized as either AT0, AK1, or non-shadowed. No significant difference found
df3_combined_long <- df3_combined_long %>%
  mutate(postproduction_label = case_when(
    Phase == "baseline" ~ "Participant Baseline",
    condition == "postproductions_AT0" ~ "Postproduction HP",
    condition == "postproductions_AK1" ~ "Postproduction LP",
    Phase == "postproductions" & voice == "None" ~ "Postproduction Non-Shadowed",
    TRUE ~ NA_character_
  )) %>%
  mutate(postproduction_label = factor(postproduction_label, levels = c(
    "Participant Baseline", "Postproduction HP", "Postproduction LP", "Postproduction Non-Shadowed"
  )))


p_postproductions_only <- ggplot() + 
  geom_smooth(
    data = df3_combined_long%>%
      filter(!is.na(postproduction_label)), aes(x = step, y = F0, color = postproduction_label, linetype = postproduction_label),
    linewidth = 1, se = F, span = 0.5
  ) +
  labs(
    title = "F0 Contours for Postproductions",
    x = "Timestep", y = "F0 (Hz)",
    color = "Speaker/Voice", linetype = "Speaker/Voice"
  ) + scale_color_manual(
    values = c(
      "Participant Baseline" = "#da216d",
      "Postproduction HP" = "#13a5dc",
      "Postproduction LP" = "#ffc002",
      "Postproduction Non-Shadowed" = "#007988"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "Participant Baseline" = "solid",
      "Postproduction HP" = "dashed",
      "Postproduction LP" = "solid",
      "Postproduction Non-Shadowed" = "dotdash"
    )
  ) + my_theme

print(p_postproductions_only)








#####--------------Shadow Iteration Plots --------------------------####

#Create a new data column to store a new variable called Iteration Label. Use iteration_label as the linetype and color variable for these plots to allow ggplot to plot intuitively and not get messy

df3_combined_long <- df3_combined_long %>%
  mutate(iteration_label = case_when(
    condition == "baseline_AT0" ~ "Baseline HP",
    condition == "baseline_AK1" ~ "Baseline LP",
    condition == "exemplar_AT0" ~ "High Prestige Voice",
    condition == "exemplar_AK1" ~ "Low Prestige Voice",
    condition == "postproductions_AT0" ~ "Postproduction HP",
    condition == "postproductions_AK1" ~ "Postproduction LP",
    Phase == "shadow" & as.numeric(iteration) == 1 ~ "Shadow Iteration 1",
    Phase == "shadow" & as.numeric(iteration) == 2 ~ "Shadow Iteration 2",
    Phase == "shadow" & as.numeric(iteration) == 3 ~ "Shadow Iteration 3",
    Phase == "shadow" & as.numeric(iteration) == 4 ~ "Shadow Iteration 4",
    TRUE ~ as.character(iteration)
  )) %>%
  mutate(iteration_label = factor(iteration_label, levels = c(
    "Baseline HP", "Baseline LP","High Prestige Voice", "Low Prestige Voice","Shadow Iteration 1", "Shadow Iteration 2", 
    "Shadow Iteration 3", "Shadow Iteration 4", "Postproduction HP", "Postproduction LP"
  )))



p_AT0_shadow_iterations <- ggplot() + 
  geom_smooth(
    data = df3_combined_long %>% filter(voice == "AT0" & iteration_label != "Shadow Iteration 4"), 
    aes(x = step, y = F0, color = iteration_label, linetype = iteration_label),
    linewidth = 1, se = FALSE, span = 0.5
  ) +
  labs(
    title = "F0 Contours for Various Shadow Iterations (HP)",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase / Iteration", linetype = "Phase / Iteration"
  ) +
  scale_color_manual(
    values = c(
      "Baseline HP" = "#da216d",
      "High Prestige Voice" = "#13a5dc",
      "Shadow Iteration 1" = "#ffc002",
      "Shadow Iteration 2" = "#93c02d",
      "Shadow Iteration 3" = "#007988",
      "Postproduction HP" = "#012060"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "Baseline HP" = "solid",
      "High Prestige Voice" = "dashed",
      "Shadow Iteration 1" = "solid",
      "Shadow Iteration 2" = "dashed",
      "Shadow Iteration 3" = "dotdash",
      "Postproduction HP" = "longdash"
    )
  ) + my_theme

print(p_AT0_shadow_iterations)



p_AK1_shadow_iterations <- ggplot() + 
  geom_smooth(
    data = df3_combined_long %>% filter(voice == "AK1"), 
    aes(x = step, y = F0, color = iteration_label, linetype = iteration_label),
    linewidth = 1, se = FALSE, span = 0.5
  ) +
  labs(
    title = "F0 Contours for Various Shadow Iterations (LP)",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase / Iteration", linetype = "Phase / Iteration"
  ) +
  scale_color_manual(
    values = c(
      "Baseline LP" = "#da216d",
      "Low Prestige Voice" = "#13a5dc",
      "Shadow Iteration 1" = "#ffc002",
      "Shadow Iteration 2" = "#93c02d",
      "Shadow Iteration 3" = "#007988",
      "Postproduction LP" = "#012060"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "Baseline LP" = "solid",
      "Low Prestige Voice" = "dashed",
      "Shadow Iteration 1" = "solid",
      "Shadow Iteration 2" = "dashed",
      "Shadow Iteration 3" = "dotdash",
      "Postproduction LP" = "longdash"
    )
  ) + my_theme

print(p_AK1_shadow_iterations)



####--------------Lexical Frequency Plots---------------####

#---------Frequency Column-------------#
df3_combined_long$Level_of_Freq[df3_combined_long$Frequency >= 800] <- "High Frequency Words"
df3_combined_long$Level_of_Freq[df3_combined_long$Frequency < 800 & df3_combined_long$Frequency >= 10] <- "Avg Frequency Words"
df3_combined_long$Level_of_Freq[df3_combined_long$Frequency < 10 | is.na(df3_combined_long$Frequency)] <- "Low Frequency Words"


df3_combined_long <- df3_combined_long %>%  mutate(frequency_label = case_when (
  condition == "baseline_AT0" ~ "Baseline HP",
  condition == "baseline_AK1" ~ "Baseline LP",
  condition == "exemplar_AT0" ~ "High Prestige Voice",
  condition == "exemplar_AK1" ~ "Low Prestige Voice",
  Phase == "shadow" ~ Level_of_Freq,
  Phase == "postproductions" ~ Level_of_Freq,
  
))%>%
  mutate(frequency_label = factor(frequency_label, levels = c(
    "Baseline HP", "Baseline LP", "High Prestige Voice", "Low Prestige Voice", "High Frequency Words", "Avg Frequency Words", 
    "Low Frequency Words")))  #Adjust the order of the variables in the legend



p_AT0_frequency_exemplar_and_shadow <- ggplot() + 
  geom_smooth(data = df3_combined_long %>% filter(condition == "shadow_AT0" | condition == "exemplar_AT0" | condition == "baseline_AT0"), mapping = aes(x=step,y=F0,color= frequency_label, linetype = frequency_label),
              linewidth=1,se=F, span=0.5)  +
  labs(
    title = "F0 Contours for Various Word Frequencies (Shadow, HP)",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase", linetype = "Phase"
  ) + 
  scale_color_manual(
    values = c(
      "Baseline HP" = "#da216d",
      "High Prestige Voice" = "#13a5dc",
      "High Frequency Words" = "#007988",
      "Avg Frequency Words" = "#93c02d",
      "Low Frequency Words" = "#f29813"
    ),
    labels = c(
      "Baseline HP", 
      "High Prestige Voice",
      "High Frequency Words",
      "Avg Frequency Words",
      "Low Frequency Words"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "Baseline HP" = "solid",
      "High Prestige Voice" = "dashed",
      "High Frequency Words" = "twodash",
      "Avg Frequency Words" = "dotdash",
      "Low Frequency Words" = "solid"
    ),
    labels = c(
      "Baseline HP", 
      "High Prestige Voice",
      "High Frequency Words",
      "Avg Frequency Words",
      "Low Frequency Words"
    )
  )+ my_theme

print(p_AT0_frequency_exemplar_and_shadow )



p_AK1_frequency_exemplar_and_shadow <- ggplot() + 
  geom_smooth(data = df3_combined_long %>% filter(condition == "shadow_AK1" | condition == "exemplar_AK1" | condition == "baseline_AK1"), mapping = aes(x=step,y=F0,color= frequency_label, linetype = frequency_label),
              linewidth=1,se=F, span=0.5)  +
  labs(
    title = "F0 Contours for Various Word Frequencies (Shadow, LP)",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase", linetype = "Phase"
  ) +scale_color_manual(
    values = c(
      "Baseline LP" = "#da216d",
      "Low Prestige Voice" = "#13a5dc",
      "High Frequency Words" = "#007988",
      "Avg Frequency Words" = "#93c02d",
      "Low Frequency Words" =  "#f29813"
    ),
    labels = c(
      "Baseline LP", 
      "Low Prestige Voice",
      "High Frequency Words",
      "Avg Frequency Words",
      "Low Frequency Words"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "Baseline LP" = "solid",
      "Low Prestige Voice" = "dashed",
      "High Frequency Words" = "twodash",
      "Avg Frequency Words" = "dotdash",
      "Low Frequency Words" = "solid"
    ),
    labels = c(
      "Baseline LP", 
      "Low Prestige Voice",
      "High Frequency Words",
      "Avg Frequency Words",
      "Low Frequency Words"
    )
  )+ my_theme

print(p_AK1_frequency_exemplar_and_shadow )





p_AT0_frequency_postproduction <- ggplot() + 
  geom_smooth(data = df3_combined_long %>% filter(condition == "postproductions_AT0" | condition == "exemplar_AT0" | condition == "baseline_AT0"), mapping = aes(x=step,y=F0,color= frequency_label, linetype = frequency_label),
              linewidth=1,se=F, span=0.5)  +
  coord_cartesian(ylim = c(120, 210)) +
  labs(
    title = "F0 Contours for Various Word Frequencies (Postproductions, HP)",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase", linetype = "Phase"
  ) + scale_color_manual(
    values = c(
      "Baseline HP" = "#da216d",
      "High Prestige Voice" = "#13a5dc",
      "High Frequency Words" = "#007988",
      "Avg Frequency Words" = "#93c02d",
      "Low Frequency Words" = "#f29813"
    ),
    labels = c(
      "Baseline HP", 
      "High Prestige Voice",
      "High Frequency Words",
      "Avg Frequency Words",
      "Low Frequency Words"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "Baseline HP" = "solid",
      "High Prestige Voice" = "dashed",
      "High Frequency Words" = "twodash",
      "Avg Frequency Words" = "dotdash",
      "Low Frequency Words" = "solid"
    ),
    labels = c(
      "Baseline HP", 
      "High Prestige Voice",
      "High Frequency Words",
      "Avg Frequency Words",
      "Low Frequency Words"
    )
  ) + my_theme
print(p_AT0_frequency_postproduction)



p_AK1_frequency_postproduction <- ggplot() + 
  geom_smooth(data = df3_combined_long %>% filter(condition == "postproductions_AK1" | condition == "exemplar_AK1" | condition == "baseline_AK1"), mapping = aes(x=step,y=F0,color= frequency_label, linetype = frequency_label),
              linewidth=1,se=F, span=0.5)  +
  labs(
    title = "F0 Contours for Various Word Frequencies (Postproduction, LP)",
    x = "Timestep", y = "F0 (Hz)",
    color = "Phase", linetype = "Phase"
  ) +scale_color_manual(
    values = c(
      "Baseline LP" = "#da216d",
      "Low Prestige Voice" = "#13a5dc",
      "High Frequency Words" = "#007988",
      "Avg Frequency Words" = "#93c02d",
      "Low Frequency Words" = "#f29813"
    ),
    labels = c(
      "Baseline LP", 
      "Low Prestige Voice",
      "High Frequency Words",
      "Avg Frequency Words",
      "Low Frequency Words"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "Baseline LP" = "solid",
      "Low Prestige Voice" = "dashed",
      "High Frequency Words" = "twodash",
      "Avg Frequency Words" = "dotdash",
      "Low Frequency Words" = "solid"
    ),
    labels = c(
      "Baseline LP", 
      "Low Prestige Voice",
      "High Frequency Words",
      "Avg Frequency Words",
      "Low Frequency Words"
    )
  )+ my_theme

print(p_AK1_frequency_postproduction)




