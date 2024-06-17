import React, { useState } from 'react';
import axios from 'axios';
import 'onsenui/css/onsenui.css';
import 'onsenui/css/onsen-css-components.css';
import 'animate.css';
import '../styles/styles.css'; 
import { Page, Button, Input, Tabbar, Tab, Segment } from 'react-onsenui'; 

const WelcomeScreen = ({ onNext }) => (
  <Page className="page">
    <div className="container">
      <div className="section section1">
        <h2 className='animate__animated animate__fadeIn'>Welcome to TARS</h2>
      </div>
      <div className="section section2">
        <p style={{ fontSize: '18px', margin: '30px 0' }} className='colorful animate__animated animate__pulse'>WE ARE HIRING!</p>
        <Button className="btn-hover color-1 animate__animated animate__fadeInUp" onClick={onNext}>Let's get started!</Button>
      </div>
      <div className="section section3">
        <p className="footer-text animate__animated animate__fadeInUp">This process takes no longer than a minute</p>
      </div>
    </div>
  </Page>
);

const NameScreen = ({ onNext, name, setName }) => (
  <Page className="page">
    <div className="container">
      <div className="section section1">
        <h2>What's your name?</h2>
      </div>
      <div className="section section2">
        <Input
          className="input"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
          float
        />
      </div>
      <div className="section section3">
        <Button className="button" onClick={onNext}>Next</Button>
      </div>
    </div>
  </Page>
);

const EmailScreen = ({ onNext, email, setEmail, name }) => (
  <Page className="page">
    <div className="container">
      <div className="section section1">
        <h2>What's your email address?</h2>
      </div>
      <div className="section section2">
        <Input
          className="input"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          type="email"
          float
        />
      </div>
      <div className="section section3">
        <Button className="button" onClick={onNext}>Next</Button>
      </div>
    </div>
  </Page>
);

const ELevelScreen = ({ onFinish, eLevel, setELevel, name, email }) => (
  <Page className="page">
    <div className="container">
      <div className="section section1">
        <h2>What's your english level?</h2>
      </div>
      <div className="section section2">
        <Segment modifier="material">
          <button onClick={() => setELevel(1)}>Basic</button>
          <button onClick={() => setELevel(2)}>Intermediate</button>
          <button onClick={() => setELevel(3)}>I'm a PRO!</button>
        </Segment>
      </div>
      <div className="section section3">
        <Button className="button" onClick={() => onFinish(name, email, eLevel)}>Finish</Button>
      </div>
    </div>
  </Page>
);

const FinishScreen = () => (
  <Page className="page">
    <div className="container">
      <div className="section section1">
        <h2>Thank you!</h2>
      </div>
      <div className="section section2">
        <p>That's all for now. <br />We'll get in touch with you soon.</p>
        <p>As simple as 1, 2, 3.</p>
      </div>
      <div className="section section3">
        <h2>- TARS -</h2>
      </div>
    </div>
  </Page>
);

export const MyApp = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [eLevel, setELevel] = useState('1');

  const handleFinish = async (name, email, eLevel) => {
    console.log('Name:', name);
    console.log('Email:', email);
    console.log('ELevel:', eLevel);

    const applicantData = {
      name,
      email,
      eLevel: eLevel.toString()
    };

    try {
      const response = await axios.post('http://127.0.0.1:8500/applicant/add', applicantData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.status === 200) {
        console.log('Success:', response.data);
        setActiveIndex(4); 
      } else {
        console.error('Error:', response.status, response.data);
      }
    } catch (error) {
      if (error.response) {
        console.error('Error response:', error.response);
      } else {
        console.error('Error:', error.message);
      }
    }
    
  };

  const renderTabs = () => [
    {
      content: <WelcomeScreen onNext={() => setActiveIndex(1)} />,
      tab: <Tab key="welcome" />
    },
    {
      content: <NameScreen name={name} setName={setName} onNext={() => setActiveIndex(2)} />,
      tab: <Tab key="name" />
    },
    {
      content: <EmailScreen email={email} setEmail={setEmail} onNext={() => setActiveIndex(3)} />,
      tab: <Tab key="email" />
    },
    {
      content: <ELevelScreen eLevel={eLevel} setELevel={setELevel} onFinish={handleFinish} name={name} email={email}/>,
      tab: <Tab key="eLevel" />
    },
    {
      content: <FinishScreen />,
      tab: <Tab key="finish" />
    }
  ];

  const toggleFooter = () => {
    setShowFooter(false);
  };

  return (
    <Tabbar
      swipeable={false}
      position='bottom'
      index={activeIndex}
      renderTabs={renderTabs}
      ignoreEdgeWidth={50}
    />
  );
};
