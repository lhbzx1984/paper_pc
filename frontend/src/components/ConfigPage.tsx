import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, message, Descriptions, Divider, Upload, Space } from 'antd';
import { SaveOutlined, DownloadOutlined, UploadOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import axios from 'axios';

interface Config {
  llm_model: string;
  llm_base_url: string;
  evaluation_criteria: Array<{
    name: string;
    weight: number;
    max_score: number;
    description: string;
  }>;
}

const ConfigPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState<Config | null>(null);
  const [importing, setImporting] = useState(false);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await axios.get('/api/config');
      setConfig(response.data);
    } catch (error) {
      message.error('获取配置失败');
    }
  };

  const handleSubmit = async (values: any) => {
    setLoading(true);
    try {
      await axios.post('/api/config', values);
      message.success('配置更新成功！');
      fetchConfig();
    } catch (error: any) {
      message.error(error.response?.data?.detail || '配置更新失败');
    } finally {
      setLoading(false);
    }
  };

  // 导出评审标准模版
  const handleExport = async () => {
    try {
      const response = await axios.get('/api/criteria/export', {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', '评审标准模版.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      message.success('评审标准模版导出成功');
    } catch (error) {
      message.error('导出失败，请确认后端服务正常运行');
    }
  };

  // 导入评审标准
  const handleImport = async (file: File) => {
    setImporting(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await axios.post('/api/criteria/import', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      if (response.data.success) {
        message.success(response.data.message);
        // 直接用返回的数据更新，同时再拉一次确保同步
        if (response.data.evaluation_criteria) {
          setConfig(prev => prev ? { ...prev, evaluation_criteria: response.data.evaluation_criteria } : prev);
        }
        fetchConfig();
      }
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      message.error(detail || '导入失败，请检查文件格式是否正确');
    } finally {
      setImporting(false);
    }
    return false;
  };

  const importProps: UploadProps = {
    accept: '.xlsx,.xls',
    showUploadList: false,
    beforeUpload: (file) => {
      handleImport(file);
      return false;
    },
  };

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      <Card title="大模型配置">
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            label="API Key"
            name="llm_api_key"
            rules={[{ required: true, message: '请输入API Key' }]}
          >
            <Input.Password placeholder="请输入大模型API Key" />
          </Form.Item>

          <Form.Item
            label="API Base URL"
            name="llm_base_url"
            rules={[{ required: true, message: '请输入API Base URL' }]}
            initialValue="https://api.openai.com/v1"
          >
            <Input placeholder="例如: https://api.openai.com/v1" />
          </Form.Item>

          <Form.Item
            label="模型名称"
            name="llm_model"
            rules={[{ required: true, message: '请输入模型名称' }]}
            initialValue="gpt-4"
          >
            <Input placeholder="例如: gpt-4, gpt-3.5-turbo" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
              保存配置
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {config && (
        <>
          <Card title="当前配置" style={{ marginTop: 24 }}>
            <Descriptions column={1} bordered>
              <Descriptions.Item label="模型">
                {config.llm_model}
              </Descriptions.Item>
              <Descriptions.Item label="API地址">
                {config.llm_base_url}
              </Descriptions.Item>
            </Descriptions>
          </Card>

          <Card
            title="评审标准"
            style={{ marginTop: 24 }}
            extra={
              <Space>
                <Button icon={<DownloadOutlined />} onClick={handleExport}>
                  导出模版
                </Button>
                <Upload {...importProps}>
                  <Button icon={<UploadOutlined />} loading={importing}>
                    导入标准
                  </Button>
                </Upload>
              </Space>
            }
          >
            {config.evaluation_criteria.map((criterion, index) => (
              <div key={index}>
                <Descriptions column={2} bordered>
                  <Descriptions.Item label="评审项" span={2}>
                    <strong>{criterion.name}</strong>
                  </Descriptions.Item>
                  <Descriptions.Item label="权重">
                    {(criterion.weight * 100).toFixed(0)}%
                  </Descriptions.Item>
                  <Descriptions.Item label="满分">
                    {criterion.max_score}分
                  </Descriptions.Item>
                  <Descriptions.Item label="说明" span={2}>
                    {criterion.description}
                  </Descriptions.Item>
                </Descriptions>
                {index < config.evaluation_criteria.length - 1 && <Divider />}
              </div>
            ))}
            <p style={{ marginTop: 16, color: '#666' }}>
              提示：可点击右上角"导出模版"下载当前标准，修改后通过"导入标准"上传更新
            </p>
          </Card>
        </>
      )}
    </div>
  );
};

export default ConfigPage;
