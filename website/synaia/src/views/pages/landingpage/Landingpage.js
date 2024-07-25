import React from 'react';
import PageContainer from 'src/components/container/PageContainer';

// components
import Banner from '../../../components/landingpage/banner/Banner';
import C2a from '../../../components/landingpage/c2a/C2a';
import C2a2 from '../../../components/landingpage/c2a/C2a2';
import DemoSlider from '../../../components/landingpage/demo-slider/DemoSlider';
import Features from '../../../components/landingpage/features/Features';
import Footer2 from '../../../components/landingpage/footer/Footer2';
import Frameworks from '../../../components/landingpage/frameworks/Frameworks';
import LpHeader from '../../../components/landingpage/header/Header';
import Testimonial from '../../../components/landingpage/testimonial/Testimonial';

const Landingpage = () => {
  return (
    <PageContainer title="Welcome to Synaia" description="Synaia landing page">
      <LpHeader />
      <Banner />
      <Features />
      <DemoSlider />
      <Frameworks />
      {/*<Testimonial />
      
       <C2a /> */}
      <C2a2 />
      <Footer2 />
    </PageContainer>
  );
};

export default Landingpage;
