library(ggplot2)

data = read.csv("/Users/amytelck/Documents/Johns Hopkins/Applied Game Theory/Project/daytona24_gametheory/data/positions.csv")

ggplot(data, aes(x = Time / 60^2, y = -1*Position, group = as.factor(Team), color = as.factor(Team))) +
  geom_line() + 
  scale_x_continuous(expand = c(0,0)) +
  scale_y_continuous(expand = c(0, 1), breaks = c(-50, -40, -30, -20, -10, -1), labels = c(50, 40, 30, 20, 10, 1)) +
  labs(title = "Position of Each Team", x = "Hour", y = "Position", color = "Team") +
  theme_bw()
