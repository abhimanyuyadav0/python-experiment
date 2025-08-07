"use client";

import Modal from "@/components/modal";
import { useAuth } from "@/contexts/AuthContext";
import { FileJson, FileText, XIcon, Upload, File, Download, Trash2 } from "lucide-react";
import React, { useState, useRef, useEffect } from "react";
import generatePDF from "react-to-pdf";
import { uploadFile, getUserFiles, deleteFile as deleteFileService, downloadFile as downloadFileService, FileResponse, testFileAuth } from "@/lib/api/services/fileServices";

interface MedicalReport {
  patientId: string;
  patientName: string;
  dateOfBirth: string;
  gender: string;
  contactNumber: string;
  email: string;
  address: string;
  reportDate: string;
  vitalSigns: {
    bloodPressure: string;
    heartRate: number;
    temperature: number;
    respiratoryRate: number;
    oxygenSaturation: number;
    weight: number;
    height: number;
    bmi: number;
  };
  labResults: {
    hemoglobin: number;
    whiteBloodCells: number;
    platelets: number;
    glucose: number;
    creatinine: number;
    cholesterol: number;
    sodium: number;
    potassium: number;
  };
  medicalNotes: string;
  diagnosis: string;
  treatment: string;
  medications: string[];
  followUpDate: string;
  doctorName: string;
  doctorSpecialty: string;
}

const CreateDataPage = () => {
  const [medicalReport, setMedicalReport] = useState<MedicalReport | null>(
    null
  );
  const [isGenerating, setIsGenerating] = useState(false);
  const [showJsonModal, setShowJsonModal] = useState(false);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string>("");
  const [uploadedFiles, setUploadedFiles] = useState<FileResponse[]>([]);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [isLoadingFiles, setIsLoadingFiles] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { token } = useAuth();

  // Load files on component mount
  useEffect(() => {
    console.log("CreateDataPage: useEffect triggered, token:", token ? "exists" : "null");
    if (token) {
      listUploadedFiles();
    }
  }, [token]);

  // Format file size
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const generateRandomName = () => {
    const firstNames = [
      "Amit",
      "Pooja",
      "Rahul",
      "Anjali",
      "Vikas",
      "Shivani",
      "Rakesh",
      "Neha",
      "Sanjay",
      "Priya",
      "Arjun",
      "Kavita",
      "Manoj",
      "Ritu",
      "Deepak",
      "Suman",
      "Ashok",
      "Meena",
      "Vivek",
      "Shalini",
      "Rohit",
      "Swati",
      "Aditya",
      "Nisha",
      "Pradeep",
      "Reena",
      "Saurabh",
      "Komal",
      "Vinod",
      "Anita",
      "Gaurav",
      "Jyoti",
      "Sunil",
      "Preeti",
      "Ajay",
      "Sonam",
      "Naveen",
      "Monika",
      "Alok",
      "Seema",
    ];

    const lastNames = [
      "Yadav",
      "Singh",
      "Verma",
      "Sharma",
      "Gupta",
      "Mishra",
      "Pandey",
      "Khan",
      "Chauhan",
      "Patel",
      "Tiwari",
      "Maurya",
      "Srivastava",
      "Rathore",
      "Dubey",
      "Jaiswal",
      "Pal",
      "Tripathi",
      "Kumar",
      "Rai",
      "Dwivedi",
      "Bajpai",
      "Ansari",
      "Siddiqui",
      "Kushwaha",
      "Pathak",
      "Nigam",
      "Qureshi",
      "Bind",
      "Shukla",
      "Saini",
      "Agrawal",
      "Vishwakarma",
      "Prajapati",
      "Rawat",
      "Malik",
      "Choudhary",
      "Gaur",
      "Bharti",
      "Upadhyay",
    ];

    return `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${
      lastNames[Math.floor(Math.random() * lastNames.length)]
    }`;
  };

  const generateRandomDate = (startYear: number, endYear: number) => {
    const start = new Date(startYear, 0, 1);
    const end = new Date(endYear, 11, 31);
    const randomDate = new Date(
      start.getTime() + Math.random() * (end.getTime() - start.getTime())
    );
    return randomDate.toISOString().split("T")[0];
  };

  const generateMedicalReport = () => {
    setIsGenerating(true);

    // Simulate API call delay
    setTimeout(() => {
      const report: MedicalReport = {
        patientId: `P${Math.floor(Math.random() * 100000)
          .toString()
          .padStart(5, "0")}`,
        patientName: generateRandomName(),
        dateOfBirth: generateRandomDate(1950, 2000),
        gender: Math.random() > 0.5 ? "Male" : "Female",
        contactNumber: `+1-${Math.floor(Math.random() * 900) + 100}-${
          Math.floor(Math.random() * 900) + 100
        }-${Math.floor(Math.random() * 9000) + 1000}`,
        email: `patient${Math.floor(Math.random() * 1000)}@email.com`,
        address: `${Math.floor(Math.random() * 9999) + 1} ${
          ["Main St", "Oak Ave", "Pine Rd", "Elm St", "Cedar Ln"][
            Math.floor(Math.random() * 5)
          ]
        }, ${
          ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"][
            Math.floor(Math.random() * 5)
          ]
        }, ${["NY", "CA", "IL", "TX", "AZ"][Math.floor(Math.random() * 5)]} ${
          Math.floor(Math.random() * 90000) + 10000
        }`,
        reportDate: new Date().toISOString().split("T")[0],
        vitalSigns: {
          bloodPressure: `${Math.floor(Math.random() * 40) + 110}/${
            Math.floor(Math.random() * 20) + 60
          }`,
          heartRate: Math.floor(Math.random() * 40) + 60,
          temperature: Math.round((Math.random() * 3 + 97) * 10) / 10,
          respiratoryRate: Math.floor(Math.random() * 10) + 12,
          oxygenSaturation: Math.floor(Math.random() * 10) + 90,
          weight: Math.floor(Math.random() * 100) + 50,
          height: Math.floor(Math.random() * 30) + 150,
          bmi: Math.round((Math.random() * 15 + 18) * 10) / 10,
        },
        labResults: {
          hemoglobin: Math.round((Math.random() * 5 + 12) * 10) / 10,
          whiteBloodCells: Math.floor(Math.random() * 8000) + 4000,
          platelets: Math.floor(Math.random() * 150000) + 150000,
          glucose: Math.floor(Math.random() * 100) + 70,
          creatinine: Math.round((Math.random() * 1.5 + 0.6) * 100) / 100,
          cholesterol: Math.floor(Math.random() * 100) + 150,
          sodium: Math.floor(Math.random() * 20) + 135,
          potassium: Math.round((Math.random() * 2 + 3.5) * 10) / 10,
        },
        medicalNotes: [
          "Patient presents with mild symptoms. No significant findings on physical examination.",
          "Patient reports feeling well. All systems functioning normally.",
          "Patient has minor complaints but overall health appears stable.",
          "Routine checkup completed. Patient is in good health.",
          "Patient shows improvement from previous visit. Continue current treatment plan.",
        ][Math.floor(Math.random() * 5)],
        diagnosis: [
          "Hypertension - Well controlled",
          "Type 2 Diabetes - Stable",
          "Hyperlipidemia - Under control",
          "No active medical conditions",
          "Mild seasonal allergies",
        ][Math.floor(Math.random() * 5)],
        treatment: [
          "Continue current medications and lifestyle modifications",
          "Monitor blood pressure and maintain low-sodium diet",
          "Regular exercise and balanced diet recommended",
          "Annual follow-up scheduled",
          "No treatment required at this time",
        ][Math.floor(Math.random() * 5)],
        medications: [
          "Lisinopril 10mg daily",
          "Metformin 500mg twice daily",
          "Atorvastatin 20mg daily",
          "Aspirin 81mg daily",
          "No medications",
        ].slice(0, Math.floor(Math.random() * 3) + 1),
        followUpDate: new Date(
          Date.now() + Math.random() * 90 * 24 * 60 * 60 * 1000
        )
          .toISOString()
          .split("T")[0],
        doctorName: `Dr. ${generateRandomName()}`,
        doctorSpecialty: [
          "Cardiology",
          "Internal Medicine",
          "Family Medicine",
          "Endocrinology",
          "General Practice",
        ][Math.floor(Math.random() * 5)],
      };

      setMedicalReport(report);
      setIsGenerating(false);
    }, 1500);
  };

  const handlePrintPdf = async () => {
    if (!medicalReport || !reportRef.current) return;

    setIsGeneratingPdf(true);

    try {
      // Simple configuration that should work reliably
      const options = {
        filename: `medical_report_${medicalReport.patientName.replace(
          /\s+/g,
          "_"
        )}_${medicalReport.reportDate}.pdf`,
        page: {
          margin: 10,
          format: "a4",
        },
        canvas: {
          scale: 1.5,
          useCORS: true,
          allowTaint: true,
          backgroundColor: "#ffffff",
        },
      };

      console.log("Starting PDF generation with options:", options);
      await generatePDF(reportRef, options);
      console.log("PDF generated successfully");
    } catch (error) {
      console.error("Error generating PDF:", error);

      // Try alternative approach with minimal options
      try {
        console.log("Trying alternative PDF generation approach...");
        await generatePDF(reportRef, {
          filename: `medical_report_${medicalReport.patientName.replace(
            /\s+/g,
            "_"
          )}_${medicalReport.reportDate}.pdf`,
        });
        console.log("Alternative PDF generation successful");
      } catch (fallbackError) {
        console.error("Fallback PDF generation also failed:", fallbackError);

        // Final fallback: Use browser print
        try {
          console.log("Trying browser print as final fallback...");
          const printWindow = window.open("", "_blank");
          if (printWindow && reportRef.current) {
            const reportContent = reportRef.current.innerHTML;
            printWindow.document.write(`
              <html>
                <head>
                  <title>Medical Report - ${medicalReport.patientName}</title>
                  <style>
                    * {
                      margin: 0;
                      padding: 0;
                      box-sizing: border-box;
                    }
                    
                    body { 
                      font-family: Arial, sans-serif; 
                      line-height: 1.6;
                      color: #333;
                      background: white;
                      padding: 20mm;
                      max-width: 200mm;
                      margin: 0 auto;
                    }
                    
                    .hospital-header {
                      text-align: center;
                      padding: 20px 0;
                      border-bottom: 2px solid #e5e7eb;
                      margin-bottom: 30px;
                    }
                    
                    .logo-container {
                      display: flex;
                      justify-content: center;
                      margin-bottom: 10px;
                    }
                    
                    .logo {
                      width: 32px;
                      height: 32px;
                      background: #059669;
                      border-radius: 50%;
                      display: flex;
                      align-items: center;
                      justify-content: center;
                    }
                    
                    .hospital-name {
                      font-size: 24px;
                      font-weight: bold;
                      color: #059669;
                      margin-bottom: 5px;
                    }
                    
                    .hospital-address {
                      font-size: 14px;
                      color: #666;
                      margin-bottom: 15px;
                    }
                    
                    .report-title {
                      font-size: 28px;
                      font-weight: bold;
                      color: #1f2937;
                      text-transform: uppercase;
                    }
                    
                    .section {
                      margin-bottom: 25px;
                    }
                    
                    .section-title {
                      font-size: 18px;
                      font-weight: 600;
                      color: #059669;
                      margin-bottom: 15px;
                      border-bottom: 1px solid #e5e7eb;
                      padding-bottom: 5px;
                    }
                    
                    .info-grid {
                      display: grid;
                      grid-template-columns: 1fr 1fr;
                      gap: 20px;
                    }
                    
                    .info-item {
                      margin-bottom: 8px;
                    }
                    
                    .info-label {
                      font-weight: 600;
                      color: #374151;
                    }
                    
                    .info-value {
                      color: #6b7280;
                    }
                    
                    .assessment-text, .diagnosis-text, .prescription-text {
                      color: #4b5563;
                      line-height: 1.8;
                    }
                    
                    .footer {
                      margin-top: 40px;
                      padding: 20px;
                      background: #f9fafb;
                      border-top: 1px solid #e5e7eb;
                      text-align: center;
                      font-size: 12px;
                      color: #6b7280;
                    }
                    
                    .footer p {
                      margin-bottom: 5px;
                    }
                    
                    @media print {
                      body { 
                        padding: 15mm;
                        margin: 0;
                      }
                      .section { page-break-inside: avoid; }
                      .footer { position: fixed; bottom: 0; width: 100%; }
                    }
                  </style>
                </head>
                <body>
                  <div class="hospital-header">
                    <div class="logo-container">
                      <div class="logo">
                        <svg width="20" height="20" fill="white" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                        </svg>
                      </div>
                    </div>
                    <div class="hospital-name">Evergreen Wellness Hospital</div>
                    <div class="hospital-address">123 Harmony Street Sunnyville, CA 90210 USA</div>
                    <div class="report-title">Medical Report</div>
                  </div>
                  
                  <div class="section">
                    <div class="section-title">Visit Info</div>
                    <div class="info-item">
                      <span class="info-label">Doctor's Name:</span> 
                      <span class="info-value">${
                        medicalReport.doctorName
                      }</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">Specialization:</span> 
                      <span class="info-value">${
                        medicalReport.doctorSpecialty
                      }</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">Visit Date:</span> 
                      <span class="info-value">${medicalReport.reportDate
                        .split("-")
                        .reverse()
                        .join(".")}</span>
                    </div>
                  </div>
                  
                  <div class="section">
                    <div class="section-title">Patient Info</div>
                    <div class="info-grid">
                      <div>
                        <div class="info-item">
                          <span class="info-label">Full Name:</span> 
                          <span class="info-value">${
                            medicalReport.patientName
                          }</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">Med. Number:</span> 
                          <span class="info-value">${
                            medicalReport.patientId
                          }</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">Phone:</span> 
                          <span class="info-value">${
                            medicalReport.contactNumber
                          }</span>
                        </div>
                      </div>
                      <div>
                        <div class="info-item">
                          <span class="info-label">Birth Date:</span> 
                          <span class="info-value">${medicalReport.dateOfBirth
                            .split("-")
                            .reverse()
                            .join(".")}</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">IHI:</span> 
                          <span class="info-value">${
                            Math.floor(Math.random() * 9000) + 1000
                          }-${Math.floor(Math.random() * 9000) + 1000}-${
              Math.floor(Math.random() * 9000) + 1000
            }-${Math.floor(Math.random() * 9000) + 1000}</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">Email:</span> 
                          <span class="info-value">${medicalReport.email}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="section">
                    <div class="section-title">Assessment</div>
                    <div class="assessment-text">
                      ${medicalReport.patientName.split(" ")[0]} ${
              medicalReport.patientName.split(" ")[1]
            } appears in good health with no immediate concerns during the examination. Based on the assessment, there are no significant issues detected, and vital signs are within normal ranges.
                    </div>
                  </div>
                  
                  <div class="section">
                    <div class="section-title">Diagnosis</div>
                    <div class="diagnosis-text">
                      After thorough examination, ${medicalReport.diagnosis.toLowerCase()}. The diagnosis indicates a healthy status with no evidence of underlying health issues.
                    </div>
                  </div>
                  
                  <div class="section">
                    <div class="section-title">Prescription</div>
                    <div class="prescription-text">
                      ${
                        medicalReport.medications.includes("No medications")
                          ? "No prescription is necessary at this time, as the patient is in good health with no identified medical concerns. Given the absence of any medical issues, no medication is prescribed at present."
                          : `Prescribed medications: ${medicalReport.medications.join(
                              ", "
                            )}. Follow the dosage instructions as directed by your healthcare provider.`
                      }
                    </div>
                  </div>
                  
                  <div class="footer">
                    <p>For inquiries and appointments, feel free to contact us.</p>
                    <p>phone: +1 (555) 123-4567, email: info@EvergreenWellnessHospital.com</p>
                    <p>www.EvergreenWellnessHospital.com</p>
                  </div>
                </body>
              </html>
            `);
            printWindow.document.close();

            // Wait for content to load before printing
            setTimeout(() => {
              printWindow.print();
              printWindow.close();
            }, 500);

          } else {
          }
        } catch (printError) {
          console.error("Print fallback also failed:", printError);
        }
      }
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  const handleUploadPdf = () => {
    fileInputRef.current?.click();
  };

  const handleFileSelect = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    console.log("CreateDataPage: File selected:", {
      name: file.name,
      type: file.type,
      size: file.size
    });

    // Validate file type (allow common file types)
    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain',
      'image/jpeg',
      'image/jpg',
      'image/png',
      'image/gif',
      'video/mp4',
      'audio/mpeg',
      'application/zip'
    ];
    
    if (!allowedTypes.includes(file.type)) {
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      return;
    }

    setIsUploading(true);
    setUploadStatus(`Uploading ${file.name}...`);

    try {
      console.log("CreateDataPage: Starting file upload");
      const response = await uploadFile(file);
      console.log("CreateDataPage: Upload response:", response);
      setUploadStatus("Upload successful!");

      // Add to uploaded files list
      setUploadedFiles((prev) => [...prev, response.data.file]);

      // Show uploaded files modal
      setShowUploadModal(true);
    } catch (error: any) {
      console.error("CreateDataPage: Upload error:", error);
      const errorMessage = error.response?.data?.detail || "Upload failed";
      setUploadStatus(`Upload failed: ${errorMessage}`);
    } finally {
      setIsUploading(false);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const listUploadedFiles = async () => {
    console.log("CreateDataPage: listUploadedFiles called");
    setIsLoadingFiles(true);
    try {
      const response = await getUserFiles();
      console.log("CreateDataPage: getUserFiles response:", response);
      setUploadedFiles(response.data.files);
      setShowUploadModal(true);
    } catch (error: any) {
      console.error("CreateDataPage: Error fetching files:", error);
      const errorMessage = error.response?.data?.detail || "Failed to fetch uploaded files";
    } finally {
      setIsLoadingFiles(false);
    }
  };

  const downloadFile = async (fileId: number, filename: string) => {
    try {
      const response = await downloadFileService(fileId);
      
      // Create blob and download
      const blob = new Blob([response.data], { type: response.headers['content-type'] });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error: any) {
      console.error("Error downloading file:", error);
    }
  };

  const deleteFile = async (fileId: number) => {
    if (!confirm("Are you sure you want to delete this file?")) return;

    try {
      await deleteFileService(fileId);
      
      // Remove from uploaded files list
      setUploadedFiles((prev) =>
        prev.filter((file) => file.id !== fileId)
      );
    } catch (error: any) {
      console.error("Error deleting file:", error);
    }
  };

  const testAuth = async () => {
    try {
      console.log("CreateDataPage: Testing file authentication");
      const response = await testFileAuth();
      console.log("CreateDataPage: Auth test successful:", response.data);
    } catch (error: any) {
      console.error("CreateDataPage: Auth test failed:", error);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Medical Report Data Generator
      </h1>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.mp4,.mp3,.zip"
        onChange={handleFileSelect}
        style={{ display: "none" }}
      />

      <div className="flex flex-wrap gap-4 mb-8">
        <button
          onClick={generateMedicalReport}
          disabled={isGenerating}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center gap-2"
        >
          {isGenerating ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Generating Report...
            </>
          ) : (
            <>
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
              Generate Medical Report Data
            </>
          )}
        </button>
        <button
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center gap-2"
          onClick={() => {
            setShowJsonModal(true);
          }}
        >
          <FileJson /> View JSON Data
        </button>
        <button
          className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center gap-2"
          onClick={handlePrintPdf}
          disabled={!medicalReport || isGeneratingPdf}
        >
          {isGeneratingPdf ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Generating PDF...
            </>
          ) : (
            <>
              <FileText /> Download PDF (A4)
            </>
          )}
        </button>
        <button
          onClick={handleUploadPdf}
          disabled={isUploading}
          className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center gap-2"
        >
          {isUploading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Uploading...
            </>
          ) : (
            <>
              <Upload /> Upload File
            </>
          )}
        </button>
        <button
          onClick={testAuth}
          className="bg-orange-600 hover:bg-orange-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center gap-2"
        >
          🔐 Test Auth
        </button>
        <button
          onClick={listUploadedFiles}
          disabled={isLoadingFiles}
          className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center gap-2"
        >
          {isLoadingFiles ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Loading...
            </>
          ) : (
            <>
              <File /> View Uploaded Files
            </>
          )}
        </button>
      </div>

      {/* Upload Status */}
      {uploadStatus && (
        <div
          className={`mb-4 p-3 rounded-lg ${
            uploadStatus.includes("successful")
              ? "bg-green-100 text-green-800 border border-green-200"
              : uploadStatus.includes("failed")
              ? "bg-red-100 text-red-800 border border-red-200"
              : "bg-blue-100 text-blue-800 border border-blue-200"
          }`}
        >
          {uploadStatus}
        </div>
      )}

      {medicalReport && (
        <div
          ref={reportRef}
          className="bg-white border border-gray-200 rounded-lg shadow-sm max-w-4xl mx-auto"
          style={{
            width: "210mm",
            minHeight: "297mm",
            padding: "20mm",
            margin: "0 auto",
            backgroundColor: "white",
          }}
        >
          {/* Hospital Header */}
          <div className="text-center py-8 border-b border-gray-200">
            <div className="flex justify-center mb-2">
              <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                <svg
                  className="w-5 h-5 text-white"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
            </div>
            <h2 className="text-2xl font-bold text-green-600 mb-1">
              Evergreen Wellness Hospital
            </h2>
            <p className="text-gray-600 text-sm mb-4">
              123 Harmony Street Sunnyville, CA 90210 USA
            </p>
            <h1 className="text-3xl font-bold text-gray-800">MEDICAL REPORT</h1>
          </div>

          <div className="space-y-6 mt-6">
            {/* Visit Info */}
            <div>
              <h3 className="text-lg font-semibold text-green-600 mb-3">
                Visit Info
              </h3>
              <div className="space-y-1 text-gray-700">
                <p>
                  <span className="font-medium">Doctor's Name:</span>{" "}
                  {medicalReport.doctorName}
                </p>
                <p>
                  <span className="font-medium">Specialization:</span>{" "}
                  {medicalReport.doctorSpecialty}
                </p>
                <p>
                  <span className="font-medium">Visit Date:</span>{" "}
                  {medicalReport.reportDate.split("-").reverse().join(".")}
                </p>
              </div>
            </div>

            {/* Patient Info */}
            <div>
              <h3 className="text-lg font-semibold text-green-600 mb-3">
                Patient Info
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-700">
                <div className="space-y-1">
                  <p>
                    <span className="font-medium">Full Name:</span>{" "}
                    {medicalReport.patientName}
                  </p>
                  <p>
                    <span className="font-medium">Med. Number:</span>{" "}
                    {medicalReport.patientId}
                  </p>
                  <p>
                    <span className="font-medium">Phone:</span>{" "}
                    {medicalReport.contactNumber}
                  </p>
                </div>
                <div className="space-y-1">
                  <p>
                    <span className="font-medium">Birth Date:</span>{" "}
                    {medicalReport.dateOfBirth.split("-").reverse().join(".")}
                  </p>
                  <p>
                    <span className="font-medium">IHI:</span>{" "}
                    {Math.floor(Math.random() * 9000) + 1000}-
                    {Math.floor(Math.random() * 9000) + 1000}-
                    {Math.floor(Math.random() * 9000) + 1000}-
                    {Math.floor(Math.random() * 9000) + 1000}
                  </p>
                  <p>
                    <span className="font-medium">Email:</span>{" "}
                    {medicalReport.email}
                  </p>
                </div>
              </div>
            </div>

            {/* Assessment */}
            <div>
              <h3 className="text-lg font-semibold text-green-600 mb-3">
                Assessment
              </h3>
              <p className="text-gray-700 leading-relaxed">
                {medicalReport.patientName.split(" ")[0]}{" "}
                {medicalReport.patientName.split(" ")[1]} appears in good health
                with no immediate concerns during the examination. Based on the
                assessment, there are no significant issues detected, and vital
                signs are within normal ranges.
              </p>
            </div>

            {/* Diagnosis */}
            <div>
              <h3 className="text-lg font-semibold text-green-600 mb-3">
                Diagnosis
              </h3>
              <p className="text-gray-700 leading-relaxed">
                After thorough examination,{" "}
                {medicalReport.diagnosis.toLowerCase()}. The diagnosis indicates
                a healthy status with no evidence of underlying health issues.
              </p>
            </div>

            {/* Prescription */}
            <div>
              <h3 className="text-lg font-semibold text-green-600 mb-3">
                Prescription
              </h3>
              <p className="text-gray-700 leading-relaxed">
                {medicalReport.medications.includes("No medications")
                  ? "No prescription is necessary at this time, as the patient is in good health with no identified medical concerns. Given the absence of any medical issues, no medication is prescribed at present."
                  : `Prescribed medications: ${medicalReport.medications.join(
                      ", "
                    )}. Follow the dosage instructions as directed by your healthcare provider.`}
              </p>
            </div>
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-8 py-6 border-t border-gray-200 mt-8">
            <div className="text-center text-gray-600 text-sm">
              <p className="mb-2">
                For inquiries and appointments, feel free to contact us.
              </p>
              <p>
                phone: +1 (555) 123-4567, email:
                info@EvergreenWellnessHospital.com
              </p>
              <p>www.EvergreenWellnessHospital.com</p>
            </div>
          </div>
        </div>
      )}

      {/* JSON Data Modal */}
      <Modal
        title="View JSON Data"
        isOpen={showJsonModal}
        onClose={() => {
          setShowJsonModal(false);
        }}
      >
        <pre className="mt-3 text-sm bg-gray-100 p-3 rounded overflow-x-auto">
          {JSON.stringify(medicalReport, null, 2)}
        </pre>
      </Modal>

      {/* Uploaded Files Modal */}
      <Modal
        title="Uploaded Files"
        isOpen={showUploadModal}
        onClose={() => {
          setShowUploadModal(false);
        }}
      >
        <div className="mt-3">
          {uploadedFiles.length === 0 ? (
            <p className="text-gray-500 text-center py-4">
              No files uploaded yet.
            </p>
          ) : (
            <div className="space-y-3">
              {uploadedFiles.map((file) => (
                <div
                  key={file.id}
                  className="border border-gray-200 rounded-lg p-3"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">
                        {file.original_filename}
                      </h4>
                      <p className="text-sm text-gray-500">
                        Type: {file.file_type} • Size: {formatFileSize(file.file_size)}
                      </p>
                      <p className="text-sm text-gray-500">
                        Uploaded: {new Date(file.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex gap-2 ml-4">
                      <button
                        onClick={() => downloadFile(file.id, file.original_filename)}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm flex items-center gap-1"
                      >
                        <Download className="w-3 h-3" />
                        Download
                      </button>
                      <button
                        onClick={() => deleteFile(file.id)}
                        className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm flex items-center gap-1"
                      >
                        <Trash2 className="w-3 h-3" />
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </Modal>
    </div>
  );
};

export default CreateDataPage;
