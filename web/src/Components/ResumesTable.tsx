import React from 'react';
import { Button, Table, Tag } from 'antd';
import type { TableColumnsType } from 'antd';
import { getStringColor } from '../Helpers/helpers';
import ResumeViewer from './ResumeViewer';

interface DataType {
  key: string;
  name: string;
  email: string;
  phoneNumber: string;
  category: string;
  score: number;
  summary: string;
  resumeUrl: string;
}

interface ResumesTableProps {
  applicants: any[];
}

const ResumesTable: React.FC<ResumesTableProps> = ({ applicants }) => {
  const [resumeModalOpen, setResumeModalOpen] = React.useState<boolean>(false);
  const [selectedResumeUrl, setSelectedResumeUrl] = React.useState<string>('');

  const handleViewResume = (resumeUrl: string) => {
    setSelectedResumeUrl(resumeUrl);
    setResumeModalOpen(true);
  };

  const handleCancelResumeModal = () => {
    setResumeModalOpen(false);
  };

  const columns: TableColumnsType<DataType> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
      render: (email) => <a href={`mailto:${email}`}>{email}</a>,
    },
    {
      title: 'Phone number',
      dataIndex: 'phoneNumber',
      key: 'phoneNumber',
      render: (phone) => <a href={`tel:${phone}`}>{phone}</a>,
    },
    {
      title: 'Category',
      dataIndex: 'category',
      key: 'category',
      render: (category) => <Tag color={getStringColor(category)} key={category}>{category.toUpperCase()}</Tag>,
    },
    {
      title: 'AI Score',
      dataIndex: 'score',
      key: 'score',
      render: (score) => score.toFixed(3),
    },
    {
      dataIndex: 'resumeUrl',
      key: 'resumeUrl',
      render: (resumeUrl) => <Button type="link" onClick={() => handleViewResume(resumeUrl)}>View Resume</Button>,
    },
  ];

  const data: DataType[] = applicants.map((applicant, index) => ({
    key: index.toString(),
    name: applicant.name,
    email: applicant.email,
    phoneNumber: applicant.phone_number,
    category: applicant.category,
    score: applicant.ai_score,
    summary: applicant.summary,
    resumeUrl: applicant.resume_link,
  }));

  return (
    <>
      <Table
        columns={columns}
        dataSource={data}
        expandable={{
          expandedRowRender: (record) => <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{record.summary}</pre>,
          rowExpandable: () => true,
        }}
      />
      <ResumeViewer
        open={resumeModalOpen}
        onCancel={handleCancelResumeModal}
        pdfUrl={selectedResumeUrl}
      />
    </>
  );
};

export default ResumesTable;
