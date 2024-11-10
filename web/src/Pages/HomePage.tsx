import { useState, useEffect } from "react";
import JobPostingsTable from "../Components/JobPostingsTable";
import { Button, Input, Row, Col, Space, Card } from "antd";
import axios from "axios";
import { apiUrl } from "../Helpers/helpers";
import { JobPosting } from "../Components/JobPostingsTable";

const HomePage: React.FC = () => {
    const [title, setTitle] = useState<string>('');
    const [description, setDescription] = useState<string>('');
    const [resumes, setResumes] = useState<JobPosting[]>([]);

    useEffect(() => {
        axios.get(`${apiUrl}/JobPostings/`)
            .then(res => {
                setResumes(res.data);
            });
    }, []);

    const handleSave = () => {
        axios.post(`${apiUrl}/JobPostings/`, { 'title': title, 'description': description })
            .then(res => {
                setResumes([res.data, ...resumes]);
                setTitle('');
                setDescription('');
            });
    };

    return (
        <div style={{ padding: '20px' }}>
            <Row justify="center">
                <Col span={12}>
                    <Card title="Add Job Posting" style={{ marginBottom: '20px' }}>
                        <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
                            <Input 
                                value={title} 
                                onChange={(e) => setTitle(e.target.value)} 
                                placeholder="Job Posting Title" 
                            />
                            <Input.TextArea 
                                value={description} 
                                onChange={(e) => setDescription(e.target.value)} 
                                rows={4} 
                                placeholder="Description" 
                            />
                            <Button type="primary" onClick={handleSave} block>
                                Save
                            </Button>
                        </Space>
                    </Card>
                </Col>
            </Row>
            <Row justify="center">
                <Col span={24}>
                    <Card title="Job Postings">
                        <JobPostingsTable data={resumes} />
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default HomePage;
