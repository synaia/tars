import React from 'react';
import { Typography, Box, Button, Stack, styled, useMediaQuery } from '@mui/material';
import { IconRocket } from '@tabler/icons';
import { NavLink } from 'react-router-dom';
// third party
import { motion } from 'framer-motion';
import './banner.css';

const StyledButton = styled(Button)(() => ({
  padding: '13px 48px',
  fontSize: '16px',
}));

const StyledButton2 = styled(Button)(({ theme }) => ({
  padding: '13px 48px',
  fontSize: '16px',
}));

const BannerContent = () => {
  const lgDown = useMediaQuery((theme) => theme.breakpoints.down('lg'));
  return (
    <Box mt={lgDown ? 8 : 0}>
      <motion.div
        initial={{ opacity: 0, translateY: 550 }}
        animate={{ opacity: 1, translateY: 0 }}
        transition={{
          type: 'spring',
          stiffness: 150,
          damping: 30,
        }}
      >
        <Typography variant="h6" display={'flex'} gap={1} mb={2} className="textShadow">
          <Typography color={'secondary'}>
            <IconRocket size={'21'} />
          </Typography>{' '}
          Leverage your company with AI
        </Typography>

        <Typography
          variant="h1"
          fontWeight={900}
          sx={{
            fontSize: {
              md: '54px',
            },
            lineHeight: {
              md: '60px',
            },
          }}
          className="textShadow"
        >
          Powerful &{' '}
          <Typography component={'span'} variant="none" color={'primary'} className="textShadow">
            Sophisticated solutions
          </Typography>{' '}
          created for you!
        </Typography>
      </motion.div>
      <Box pt={4} pb={3}>
        <motion.div
          initial={{ opacity: 0, translateY: 550 }}
          animate={{ opacity: 1, translateY: 0 }}
          transition={{
            type: 'spring',
            stiffness: 150,
            damping: 30,
            delay: 0.2,
          }}
        >
          <Typography variant="h5" fontWeight={300} className="textShadow2 black">
          {' '}Gain a competitive edge by scaling your operations and minimizing expenses.
          </Typography>
        </motion.div>
      </Box>
      <motion.div
        initial={{ opacity: 0, translateY: 550 }}
        animate={{ opacity: 1, translateY: 0 }}
        transition={{
          type: 'spring',
          stiffness: 150,
          damping: 30,
          delay: 0.4,
        }}
      >
        {/* <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} mt={3}>
          <StyledButton variant="contained" color="primary" to="/auth/login" component={NavLink}>
            Login
          </StyledButton>

          <StyledButton2 variant="outlined" component={NavLink} to="/dashboards/modern">
            Live Preview
          </StyledButton2>
        </Stack> */}
      </motion.div>
    </Box>
  );
};

export default BannerContent;
