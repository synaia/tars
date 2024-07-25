import React from 'react';
import {
  Box,
  FormControlLabel,
  Button,
  Grid,
  MenuItem,
  FormControl,
  Alert
} from '@mui/material';
import './forms.css';

import CustomTextField from '../../forms/theme-elements/CustomTextField';
import CustomFormLabel from '../../forms/theme-elements/CustomFormLabel';
import ParentCard from '../../shared/ParentCard';


const FbContactForm = () => {


  return (
    <div>
      {/* ------------------------------------------------------------------------------------------------ */}
      {/* Basic Checkbox */}
      {/* ------------------------------------------------------------------------------------------------ */}
      <ParentCard title="Contact Form" footer={
        <>
          <Button
            variant="contained"
            color="error"
            sx={{
              mr: 1,
            }}
            className='black'
          >
            Cancel
          </Button>
          <Button variant="contained" color="primary" className='black'>
            Send
          </Button>
        </>
      }>

        <form>
          <Grid container spacing={3} mb={3}>
            <Grid item lg={6} md={12} sm={12}>
              <CustomFormLabel htmlFor="fname-text">First Name</CustomFormLabel>
              <CustomTextField id="fname-text" variant="outlined" fullWidth />
            </Grid>
            <Grid item lg={6} md={12} sm={12}>
              <CustomFormLabel htmlFor="lname-text">Last Name</CustomFormLabel>

              <CustomTextField id="lname-text" variant="outlined" fullWidth />
            </Grid>
          </Grid>
        </form>
        <Grid container spacing={3} mb={3} mt={1}>
          <Grid item lg={12} md={12} sm={12} xs={12}>
            <CustomFormLabel
              sx={{
                mt: 0,
              }}
              htmlFor="email-address"
            >
              Email
            </CustomFormLabel>
            <CustomTextField
              id="email-address"
              helperText="We'll never share your email with anyone else."
              variant="outlined"
              fullWidth
            />
            <CustomFormLabel htmlFor="outlined-multiline-static">How can we help you?</CustomFormLabel>

            <CustomTextField
              id="outlined-multiline-static"
              multiline
              rows={4}
              variant="outlined"
              fullWidth
            />
          </Grid>
        </Grid>
      </ParentCard>
    </div>
  );
};

export default FbContactForm;
