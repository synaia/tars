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

const Service4 = () => {
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
            <CardMedia component="img" height="440" image="/src/assets/images/blog/blog-img10.jpg" alt="imag" />
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
                WhatsApp Workflows
              </Typography>
            </Box>
          </CardContent>
          <Divider />
          <CardContent>
            <p>
            At Synaia AI, we specialize in designing efficient WhatsApp workflow automation services to enhance your communication and streamline business processes. As proud partners of Meta, our expert team develops customized workflows that integrate seamlessly with WhatsApp, enabling automated responses, task assignments, and customer interactions. By leveraging the power of AI, we ensure that your WhatsApp communications are not only efficient but also highly personalized and effective.
            </p>
            <p>
            Our WhatsApp workflow solutions cover a wide range of applications, from customer support automation to marketing campaigns. Utilizing the latest technologies, we create robust workflows that save time, reduce manual efforts, and improve overall productivity. At Synaia AI, we are committed to providing high-quality WhatsApp workflow services that elevate your business operations and customer engagement. Partner with us to transform your WhatsApp communications into a powerful tool for success.
            </p>
          </CardContent>
        </>
      </BlankCard>
    </Box>
  );
};

export default Service4;
