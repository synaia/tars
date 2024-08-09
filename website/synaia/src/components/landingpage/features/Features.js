import React from 'react';
import FeaturesTitle from './FeaturesTitle';
import { Typography, Grid, Container, Box } from '@mui/material';
import {
  IconAdjustments,
  IconArchive,
  IconArrowsShuffle,
  IconBook,
  IconBuildingCarousel,
  IconCalendar,
  IconChartPie,
  IconDatabase,
  IconDiamond,
  IconLanguageKatakana,
  IconLayersIntersect,
  IconMessages,
  IconRefresh,
  IconRobot,
  IconShieldLock,
  IconMoodCrazyHappy,
  IconMoodSmile,
  IconTag,
  IconAd2,
  IconReportMedical,
  IconWand,
} from '@tabler/icons';
import AnimationFadeIn from '../animation/Animation';

const featuresData = [
  {
    icon: <IconRobot width={40} height={40} strokeWidth={1.5} />,
    title: 'Automating Routine Tasks',
    subtext: 'AI can handle repetitive tasks, allowing your employees to focus on more strategic activities and increasing overall productivity.',
  },
  {
    icon: <IconMoodSmile width={40} height={40} strokeWidth={1.5} />,
    title: 'Better Customer Experience',
    subtext: 'By analyzing customer data, AI can provide personalized recommendations and improve customer service through chatbots and virtual assistants.',
  },
  {
    icon: <IconAdjustments width={40} height={40} strokeWidth={1.5} />,
    title: 'Predictive Analytics',
    subtext: 'AI can analyze vast amounts of data to identify trends and patterns, helping businesses forecast demand, and make data-driven decisions.',
  },
  {
    icon: <IconAd2 width={40} height={40} strokeWidth={1.5} />,
    title: 'Marketing Campaigns',
    subtext: 'AI can analyze consumer behavior to create targeted marketing campaigns that resonate with individual customers, increasing engagement.',
  },
];

const Features = () => {
  return (
    <Box py={6}>
      <Container maxWidth="lg">
        <FeaturesTitle />

        <Box mt={6}>
          <Grid container spacing={3}>
            {featuresData.map((feature, index) => (
              <Grid item xs={12} sm={4} lg={3} textAlign="center" key={index}>
                <AnimationFadeIn>
                  <Box color="primary.main">{feature.icon}</Box>
                  <Typography variant="h5" mt={3}>
                    {feature.title}
                  </Typography>
                  <Typography variant="subtitle1" color="textSecondary" mt={1} mb={3}>
                    {feature.subtext}
                  </Typography>
                </AnimationFadeIn>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </Box>
  );
};

export default Features;
