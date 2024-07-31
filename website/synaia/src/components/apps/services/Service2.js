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

const Service2 = () => {
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
            <CardMedia component="img" height="440" image="/src/assets/images/blog/blog-img5.jpg" alt="imag" />
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
                AI Automations
              </Typography>
            </Box>
          </CardContent>
          <Divider />
          <CardContent>
            <p>
            At Synaia AI, we specialize in delivering cutting-edge AI automation services designed to streamline your business operations. Our professional team excels in implementing advanced AI technologies that automate repetitive tasks, enhance productivity, and reduce operational costs. We focus on creating intelligent automation solutions that are customized to meet the unique needs of your business, ensuring seamless integration and optimal performance.
            </p>
            <p>
            Our AI automation services encompass a broad range of applications, from robotic process automation (RPA) to intelligent workflow automation. By leveraging state-of-the-art technologies and methodologies, we develop solutions that not only improve efficiency but also drive innovation. At Synaia AI, we are committed to providing high-quality automation services that empower your business to achieve new levels of efficiency and success. Partner with us to transform your operations with intelligent, reliable automation solutions.
            </p>
          </CardContent>
        </>
      </BlankCard>
    </Box>
  );
};

export default Service2;
