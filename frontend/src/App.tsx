import React, { useState } from 'react';
import { Layout, Tabs } from 'antd';
import { FileTextOutlined, SettingOutlined } from '@ant-design/icons';
import UploadPage from './components/UploadPage';
import ConfigPage from './components/ConfigPage';
import './App.css';

const { Header, Content } = Layout;

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('upload');

  const items = [
    {
      key: 'upload',
      label: (
        <span>
          <FileTextOutlined />
          论文评审
        </span>
      ),
      children: <UploadPage />,
    },
    {
      key: 'config',
      label: (
        <span>
          <SettingOutlined />
          系统配置
        </span>
      ),
      children: <ConfigPage />,
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#1890ff', padding: '0 24px' }}>
        <h1 style={{ color: 'white', margin: 0, lineHeight: '64px' }}>
          毕业论文智能评审系统
        </h1>
      </Header>
      <Content style={{ padding: '24px' }}>
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={items}
          size="large"
        />
      </Content>
    </Layout>
  );
};

export default App;
