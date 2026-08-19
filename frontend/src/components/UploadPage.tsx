import React, { useState } from 'react';
import { Upload, Button, Card, message, Spin, Descriptions, Tag, Divider, Progress } from 'antd';
import { UploadOutlined, InboxOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import axios from 'axios';

const { Dragger } = Upload;

interface CriterionScore {
  name: string;
  weight: number;
  max_score: number;
  score: number;
  comment: string;
  suggestion: string;
}

interface EvaluationResult {
  total_score: number;
  grade: string;
  criteria_scores: CriterionScore[];
  overall_comment: string;
}

const UploadPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<EvaluationResult | null>(null);
  const [fileName, setFileName] = useState<string>('');

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    accept: '.doc,.docx,.pdf,.wps',
    beforeUpload: (file) => {
      const isValidType = 
        file.type === 'application/pdf' ||
        file.type === 'application/msword' ||
        file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
        file.name.endsWith('.wps');
      
      if (!isValidType) {
        message.error('只支持 Word、WPS 和 PDF 格式的文件！');
        return false;
      }

      const isLt50M = file.size / 1024 / 1024 < 50;
      if (!isLt50M) {
        message.error('文件大小不能超过 50MB！');
        return false;
      }

      handleUpload(file);
      return false;
    },
  };

  const handleUpload = async (file: File) => {
    setLoading(true);
    setResult(null);
    setFileName(file.name);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setResult(response.data.result);
        message.success('论文评审完成！');
      }
    } catch (error: any) {
      message.error(error.response?.data?.detail || '评审失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  const getGradeColor = (grade: string) => {
    const colorMap: Record<string, string> = {
      '优秀': 'green',
      '良好': 'blue',
      '中等': 'orange',
      '及格': 'gold',
      '不及格': 'red',
    };
    return colorMap[grade] || 'default';
  };

  return (
    <div className="upload-container">
      <Card>
        <Dragger {...uploadProps} disabled={loading}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
          <p className="ant-upload-hint">
            支持 Word (.doc, .docx)、WPS (.wps) 和 PDF (.pdf) 格式
          </p>
        </Dragger>
      </Card>

      {loading && (
        <Card style={{ marginTop: 24, textAlign: 'center' }}>
          <Spin size="large" />
          <p style={{ marginTop: 16 }}>正在评审论文，请稍候...</p>
        </Card>
      )}

      {result && (
        <>
          <Card className="result-card">
            <div className="score-display">
              <h2>总分</h2>
              <p className="total-score">{result.total_score}</p>
              <div className="grade-badge">
                <Tag color={getGradeColor(result.grade)} style={{ fontSize: 20, padding: '8px 16px' }}>
                  {result.grade}
                </Tag>
              </div>
            </div>
          </Card>

          <Card title="各项评分详情" className="result-card">
            {result.criteria_scores.map((criterion, index) => (
              <div key={index} style={{ marginBottom: 24 }}>
                <Descriptions column={1} bordered>
                  <Descriptions.Item label="评审项目">
                    <strong>{criterion.name}</strong>
                  </Descriptions.Item>
                  <Descriptions.Item label="得分">
                    <Progress
                      percent={(criterion.score / criterion.max_score) * 100}
                      format={() => `${criterion.score} / ${criterion.max_score}`}
                    />
                  </Descriptions.Item>
                  <Descriptions.Item label="权重">
                    {(criterion.weight * 100).toFixed(0)}%
                  </Descriptions.Item>
                  <Descriptions.Item label="评价">
                    {criterion.comment}
                  </Descriptions.Item>
                  <Descriptions.Item label="改进建议">
                    {criterion.suggestion}
                  </Descriptions.Item>
                </Descriptions>
                {index < result.criteria_scores.length - 1 && <Divider />}
              </div>
            ))}
          </Card>

          <Card title="总体评价" className="result-card">
            <p style={{ fontSize: 16, lineHeight: 1.8, whiteSpace: 'pre-wrap' }}>
              {result.overall_comment}
            </p>
          </Card>
        </>
      )}
    </div>
  );
};

export default UploadPage;
