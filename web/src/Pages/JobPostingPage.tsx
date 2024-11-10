import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Typography, Spin, message, Button, Upload, Row, Col, Space } from 'antd';
import { UploadFile } from 'antd/es/upload/interface';
import axios from 'axios';
import ResumesTable from '../Components/ResumesTable';
import { apiUrl } from '../Helpers/helpers';

const { Title, Text, Paragraph } = Typography;

const JobPostingPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [applicants, setApplicants] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);  // Initial loading state
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);

  useEffect(() => {
    const fetchJobPosting = async () => {
      if (!id) return;

      setLoading(true);
      try {
        const response = await axios.get(`${apiUrl}/JobPostings/${id}`);
        const jobPosting = response.data;
        setTitle(jobPosting.title);
        setDescription(jobPosting.description);
        setApplicants(jobPosting.applicants);
      } catch (error) {
        message.error('Failed to fetch job posting details');
      } finally {
        setLoading(false);
      }
    };

    fetchJobPosting();
  }, [id]);

  const handleFileChange = (info: any) => {
    const newFileList = info.fileList.map((file: UploadFile) => {
      if (file.response) {
        file.url = file.response.url;
      }
      return file;
    });
    setFileList(newFileList);

    if (info.file.status === 'done') {
      message.success(`${info.file.name} file uploaded successfully`);
    } else if (info.file.status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  };

  const handleUpload = () => {
    if (fileList.length === 0) {
      message.error('Please select a file to upload.');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('resume', fileList[0].originFileObj as File);

    axios.post(`${apiUrl}/JobPostings/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(() => {
      refreshApplicants();
      message.success('Resume added successfully');
    })
    .catch(() => {
      message.error('Failed to add resume');
    })
    .finally(() => {
      setUploading(false);
    });
  };

  const refreshApplicants = async () => {
    try {
      const response = await axios.get(`${apiUrl}/JobPostings/${id}`);
      setApplicants(response.data.applicants);
    } catch (error) {
      message.error('Failed to fetch updated applicants');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
          <Spin size="large" />
        </div>
      ) : (
        <>
          <Row justify="center">
            <Col span={12}>
              <Card>
                <Title level={2}>{title}</Title>
                <Paragraph style={{ maxHeight: '150px', overflowY: 'auto', whiteSpace: 'pre-wrap' }}>
                  {description}
                </Paragraph>
              </Card>
            </Col>
          </Row>
          <Row justify="center" style={{ marginTop: '20px' }}>
            <Col span={12}>
              <Card>
                {selectedFile && <Text>{selectedFile}</Text>}
                <Space direction="horizontal" size="middle" style={{ display: 'flex', marginTop: selectedFile ? '10px' : '0' }}>
                  <Upload
                    accept=".pdf"
                    fileList={fileList}
                    beforeUpload={(file) => {
                      const newFile: UploadFile = {
                        uid: file.uid,
                        name: file.name,
                        status: 'done',
                        url: URL.createObjectURL(file),
                        originFileObj: file,
                      };
                      setFileList([newFile]);
                      setSelectedFile(file.name);
                      return false;
                    }}
                    onChange={handleFileChange}
                    showUploadList={false}
                  >
                    <Button type="primary">Select PDF</Button>
                  </Upload>
                  <Button
                    type="primary"
                    onClick={handleUpload}
                    loading={uploading}
                  >
                    {uploading ? 'Adding Resume' : 'Add Resume'}
                  </Button>
                </Space>
              </Card>
            </Col>
          </Row>
          <Row justify="center" style={{ marginTop: '40px' }}>
            <Col span={24}>
              <Card>
                <Title level={3}>Applicants</Title>
                <ResumesTable applicants={applicants} />
              </Card>
            </Col>
          </Row>
        </>
      )}
    </div>
  );
};

export default JobPostingPage;
