import React, { useEffect } from 'react';
import { fetchBlogPost } from 'src/store/apps/blog/BlogSlice';
import { useLocation } from 'react-router-dom';
import {
  CardContent,
  Stack,
  Avatar,
  Typography,
  CardMedia,
  Chip,
  Tooltip,
  Box,
  Divider,
  TextField,
  Button,
  Skeleton,
} from '@mui/material';
import Breadcrumb from 'src/layouts/full/shared/breadcrumb/Breadcrumb';
import { IconEye, IconMessage2, IconPoint, IconQuote } from '@tabler/icons';
import { format } from 'date-fns';
import { uniqueId } from 'lodash';
import BlankCard from '../../shared/BlankCard';
import { useDispatch, useSelector } from 'react-redux';

const Service3 = () => {
  const dispatch = useDispatch();
  const title = useLocation();
  const getTitle = title.pathname.split('/').pop();
  const [replyTxt, setReplyTxt] = React.useState('');

  useEffect(() => {
    dispatch(fetchBlogPost(getTitle));
  }, [dispatch]);

  // Get post
  const post = useSelector((state) => state.blogReducer.selectedPost);

  const [isLoading, setLoading] = React.useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 700);
    return () => clearTimeout(timer);
  }, []);

  return (
    <Box>
      <BlankCard>
        <>
          {isLoading ? (
            <>
              <Skeleton
                animation="wave"
                variant="square"
                width="100%"
                height={440}
                sx={{ borderRadius: (theme) => theme.shape.borderRadius / 5 }}
              ></Skeleton>
            </>
          ) : (
            <CardMedia component="img" height="440" image="/src/assets/images/blog/blog-img9.jpg" alt="imag" />
          )}
          <CardContent>
            <Box my={3}>
              <Typography
                gutterBottom
                variant="h1"
                fontWeight={600}
                color="inherit"
                sx={{ textDecoration: 'none' }}
              >
                Data Science
              </Typography>
            </Box>
          </CardContent>
          <Divider />
          <CardContent>
            <p>
            At Synaia AI, we offer premier data science services that transform raw data into actionable insights. Our expert team employs advanced data analytics, machine learning, and statistical modeling to uncover patterns and trends that drive informed decision-making. We specialize in custom data science solutions tailored to your business needs, ensuring that you gain a competitive edge in your industry.
            </p>
            <p>
            Our data science services encompass a wide range of applications, from predictive analytics to data visualization. By utilizing the latest technologies and methodologies, we provide comprehensive solutions that help you understand and leverage your data effectively. At Synaia AI, we are dedicated to delivering high-quality data science services that empower your business with the knowledge and tools to succeed. Trust us to turn your data into a powerful asset, driving innovation and growth.
            </p>
          </CardContent>
        </>
      </BlankCard>
    </Box>
  );
};

export default Service3;
