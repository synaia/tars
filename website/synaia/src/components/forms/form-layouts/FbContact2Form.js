import React from 'react';
import {
  Box,
  Typography,
  FormControlLabel,
  Button,
  Grid,
  MenuItem,
  FormControl,
  Alert
} from '@mui/material';
import {
  IconPlane,
  IconMessage,
  IconLocation,
  IconGps,
  IconMapPin,
  IconPhone
} from '@tabler/icons';
import './forms.css';

import CustomTextField from '../../forms/theme-elements/CustomTextField';
import CustomFormLabel from '../../forms/theme-elements/CustomFormLabel';
import ParentCard from '../../shared/ParentCard';


const FbContact2Form = () => {


  return (

    <form>
      <Typography
        variant="h4"
        fontWeight={900}
        sx={{
          fontSize: {
            md: '20px',
          },
          lineHeight: {
            md: '60px',
          },
          
        }}
        className="textShadow"
      >
        <Typography component={'span'} variant="none" color={'primary'} className="textShadow" sx={{ color: 'white !important' }}>
          Contact Information
        </Typography>{' '}
      </Typography>
      <Grid container spacing={3} mb={3}>
        <Grid item lg={6} md={12} sm={12}>
          <Typography variant="h6" display={'flex'} gap={1} mb={2} className="textShadow">
            <Typography color={'secondary'}>
              <IconPhone size={'21'} />
            </Typography>{' '}
            <a href="tel:+18296456177" className='link'>+1 829 645-6177</a>
          </Typography>
          <Typography variant="h6" display={'flex'} gap={1} mb={2} className="textShadow">
            <Typography color={'secondary'}>
              <IconMessage size={'21'} />
            </Typography>{' '}
            <a href="mailto:info@synaia.io" className='link'>info@synaia.io</a>
          </Typography>
          <Typography variant="h6" display={'flex'} gap={1} mb={2} className="textShadow">
            <Typography color={'secondary'}>
              <IconMapPin size={'21'} />
            </Typography>{' '}
            Harju maakond, Tallinn, Kesklinna linnaosa, Tornimäe tn 5, 10145
          </Typography>
        </Grid>
        <Grid item lg={6} md={12} sm={12}>
          <div style={{ width: '100%', height: '300px' }}>
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2029.0169231476389!2d24.758567177178293!3d59.43279230273469!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4692935f7c1fdfe7%3A0xb7aca91a3e25de5c!2sTornim%C3%A4e%205%2C%2010145%20Tallinn%2C%20Estonia!5e0!3m2!1ses-419!2sdo!4v1721879743125!5m2!1ses-419!2sdo" 
            width="100%" 
            height="100%" 
            style={{ border: 0, borderRadius: '5px'}}
            allowfullscreen="" 
            loading="lazy" 
            referrerpolicy="no-referrer-when-downgrade"></iframe>
          </div>
        </Grid>
      </Grid>
    </form>
  );
};

export default FbContact2Form;
