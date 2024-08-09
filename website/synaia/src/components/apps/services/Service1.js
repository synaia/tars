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

const Service1 = () => {
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
            <CardMedia component="img" height="440" image="/src/assets/images/blog/blog-img2.jpg" alt="imag" />
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
                Sotfware Development
              </Typography>
            </Box>
          </CardContent>
          <Divider />
          <CardContent>
            <p>
            At Synaia AI, we pride ourselves on being a professional team dedicated to delivering exceptional software development services. Our expertise spans a wide range of technologies, ensuring that we can meet the diverse needs of our clients. Whether it's developing custom applications or enhancing existing systems, we leverage the latest advancements in artificial intelligence to provide innovative and efficient solutions. Our team's commitment to excellence and continuous learning ensures that we stay at the forefront of technology, ready to tackle any challenge.
            </p>
            <p>
            We specialize in custom software development, utilizing the best technologies and methodologies to create tailored solutions that drive success. From AI-driven analytics to machine learning algorithms, our comprehensive services are designed to meet the specific requirements of each project. We believe in a collaborative approach, working closely with our clients to understand their goals and deliver results that exceed expectations. With Synaia AI, you can trust that your software development needs are in capable hands, supported by a team that values quality and innovation.
            </p>
          </CardContent>
        </>
      </BlankCard>
    </Box>
  );
};

export default Service1;
