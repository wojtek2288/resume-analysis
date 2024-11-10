import React from 'react';
import { Table } from 'antd';
import type { TableColumnsType } from 'antd';
import { Link } from 'react-router-dom';

export interface JobPosting {
  id: string;
  title: string;
  description: string;
  resume_count: number;
}

interface JobPostingsTableProps {
  data: JobPosting[],
}

const columns: TableColumnsType<JobPosting> = [
  { title: 'Job posting title', dataIndex: 'title', key: 'title' },
  { title: 'Number of resumes', dataIndex: 'resume_count', key: 'resume_count' },
  {
    dataIndex: '',
    key: 'x',
    render: (text, record) => (
      <Link to={`/job-posting/${record.id}`}>Details</Link>
    ),
  },
];

const JobPostingsTable: React.FC<JobPostingsTableProps> = (props) => (
  <Table
    columns={columns}
    expandable={{
      expandedRowRender: (record) => <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{record.description}</pre>,
      rowExpandable: () => true,
    }}
    dataSource={props.data}
    rowKey="id"
  />
);

export default JobPostingsTable;
