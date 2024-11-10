import React, { useState, useEffect } from 'react';
import { Modal, Button } from 'antd';
import { Document, Page, pdfjs } from 'react-pdf';

interface ResumeViewerProps {
  open: boolean;
  onCancel: () => void;
  pdfUrl: string;
}

const ResumeViewer: React.FC<ResumeViewerProps> = ({ open, onCancel, pdfUrl }) => {
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState<number>(1);

  useEffect(() => {
    pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;
  }, []);

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  const goToPreviousPage = () => {
    setPageNumber((prevPageNumber) => Math.max(prevPageNumber - 1, 1));
  };

  const goToNextPage = () => {
    setPageNumber((prevPageNumber) => Math.min(prevPageNumber + 1, numPages));
  };

  const handleCancel = () => {
    onCancel();
    setPageNumber(1);
  };

  return (
    <Modal
      open={open}
      onCancel={handleCancel}
      footer={null}
      style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <div style={{ maxWidth: '100%' }}>
        <Document file={pdfUrl} onLoadSuccess={onDocumentLoadSuccess}>
          <Page pageNumber={pageNumber} renderAnnotationLayer={false} renderTextLayer={false} scale={1.5} />
        </Document>
        <div style={{ textAlign: 'center', marginTop: '10px' }}>
          <Button type="primary" onClick={goToPreviousPage} disabled={pageNumber <= 1}>
            Previous Page
          </Button>
          <span style={{ margin: '0 10px' }}>
            Page {pageNumber} of {numPages}
          </span>
          <Button type="primary" onClick={goToNextPage} disabled={pageNumber >= numPages}>
            Next Page
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default ResumeViewer;
