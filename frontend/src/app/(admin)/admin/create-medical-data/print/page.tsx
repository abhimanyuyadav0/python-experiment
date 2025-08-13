"use client";
import React, { useState, useRef } from "react";
import {
  FileJson,
  FileText,
  Printer,
  Download,
  Copy,
  Share2,
  Eye,
  EyeOff,
  RefreshCw,
  Save,
  Mail,
  Calendar,
  User,
  Activity,
  Stethoscope,
  Pill,
  FileX,
  X,
} from "lucide-react";
import Modal from "@/components/modal";

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

// const Modal = ({
//   title,
//   isOpen,
//   onClose,
//   children,
// }: {
//   title: string;
//   isOpen: boolean;
//   onClose: () => void;
//   children: React.ReactNode;
// }) => {
//   if (!isOpen) return null;

//   return (
//     <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
//       <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
//         <div className="flex items-center justify-between p-4 border-b">
//           <h3 className="text-lg font-semibold">{title}</h3>
//           <button
//             onClick={onClose}
//             className="p-2 hover:bg-gray-100 rounded-full transition-colors"
//           >
//             <X className="w-5 h-5" />
//           </button>
//         </div>
//         <div className="p-4 overflow-y-auto max-h-[calc(90vh-80px)]">
//           {children}
//         </div>
//       </div>
//     </div>
//   );
// };

const Button = ({
  onClick,
  disabled = false,
  variant = "primary",
  size = "md",
  children,
}: {
  onClick: () => void;
  disabled?: boolean;
  variant?: "primary" | "secondary" | "success" | "danger";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
}) => {
  const baseClasses =
    "inline-flex items-center gap-2 font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2";

  const variants = {
    primary:
      "bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500 disabled:bg-blue-300",
    secondary:
      "bg-gray-200 hover:bg-gray-300 text-gray-800 focus:ring-gray-500 disabled:bg-gray-100",
    success:
      "bg-green-600 hover:bg-green-700 text-white focus:ring-green-500 disabled:bg-green-300",
    danger:
      "bg-red-600 hover:bg-red-700 text-white focus:ring-red-500 disabled:bg-red-300",
  };

  const sizes = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-6 py-3 text-lg",
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${
        disabled ? "cursor-not-allowed opacity-60" : "hover:shadow-lg"
      }`}
    >
      {children}
    </button>
  );
};

const CreateDataPage = () => {
  const [medicalReport, setMedicalReport] = useState<MedicalReport | null>(
    null
  );
  const [isGenerating, setIsGenerating] = useState(false);
  const [showJsonModal, setShowJsonModal] = useState(false);
  const [showPreviewModal, setShowPreviewModal] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [exportFormat, setExportFormat] = useState<"pdf" | "json" | "csv">(
    "pdf"
  );
  const [savedReports, setSavedReports] = useState<MedicalReport[]>([]);
  const [showSavedReports, setShowSavedReports] = useState(false);
  const [notification, setNotification] = useState<string | null>(null);
  const reportRef = useRef<HTMLDivElement>(null);

  const showNotification = (message: string) => {
    setNotification(message);
    setTimeout(() => setNotification(null), 3000);
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
      showNotification("Medical report generated successfully!");
    }, 1500);
  };

  const handlePrint = () => {
    window.print();
    showNotification("Print dialog opened!");
  };

  const downloadAsJSON = () => {
    if (!medicalReport) return;

    const dataStr = JSON.stringify(medicalReport, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `medical_report_${medicalReport.patientName.replace(
      /\s+/g,
      "_"
    )}_${medicalReport.reportDate}.json`;
    link.click();
    URL.revokeObjectURL(url);
    showNotification("JSON file downloaded successfully!");
  };

  const downloadAsCSV = () => {
    if (!medicalReport) return;

    const csvData = [
      ["Field", "Value"],
      ["Patient ID", medicalReport.patientId],
      ["Patient Name", medicalReport.patientName],
      ["Date of Birth", medicalReport.dateOfBirth],
      ["Gender", medicalReport.gender],
      ["Contact Number", medicalReport.contactNumber],
      ["Email", medicalReport.email],
      ["Address", medicalReport.address],
      ["Report Date", medicalReport.reportDate],
      ["Blood Pressure", medicalReport.vitalSigns.bloodPressure],
      ["Heart Rate", medicalReport.vitalSigns.heartRate.toString()],
      ["Temperature", medicalReport.vitalSigns.temperature.toString()],
      ["Diagnosis", medicalReport.diagnosis],
      ["Treatment", medicalReport.treatment],
      ["Doctor Name", medicalReport.doctorName],
      ["Doctor Specialty", medicalReport.doctorSpecialty],
    ];

    const csvContent = csvData.map((row) => row.join(",")).join("\n");
    const dataBlob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `medical_report_${medicalReport.patientName.replace(
      /\s+/g,
      "_"
    )}_${medicalReport.reportDate}.csv`;
    link.click();
    URL.revokeObjectURL(url);
    showNotification("CSV file downloaded successfully!");
  };

  const copyToClipboard = () => {
    if (!medicalReport) return;

    navigator.clipboard.writeText(JSON.stringify(medicalReport, null, 2));
    showNotification("Report data copied to clipboard!");
  };

  const saveReport = () => {
    if (!medicalReport) return;

    setSavedReports((prev) => [...prev, medicalReport]);
    showNotification("Report saved successfully!");
  };

  const loadSavedReport = (report: MedicalReport) => {
    setMedicalReport(report);
    setShowSavedReports(false);
    showNotification("Report loaded successfully!");
  };

  const deleteSavedReport = (index: number) => {
    setSavedReports((prev) => prev.filter((_, i) => i !== index));
    showNotification("Report deleted!");
  };

  const clearAllReports = () => {
    setSavedReports([]);
    showNotification("All saved reports cleared!");
  };

  const shareReport = () => {
    if (!medicalReport) return;

    if (navigator.share) {
      navigator.share({
        title: `Medical Report - ${medicalReport.patientName}`,
        text: `Medical report for ${medicalReport.patientName} dated ${medicalReport.reportDate}`,
        url: window.location.href,
      });
    } else {
      copyToClipboard();
      showNotification("Report data copied for sharing!");
    }
  };

  const emailReport = () => {
    if (!medicalReport) return;

    const subject = `Medical Report - ${medicalReport.patientName}`;
    const body = `Please find the medical report details:\n\nPatient: ${
      medicalReport.patientName
    }\nDate: ${medicalReport.reportDate}\nDoctor: ${
      medicalReport.doctorName
    }\n\nFull report data:\n${JSON.stringify(medicalReport, null, 2)}`;

    window.location.href = `mailto:?subject=${encodeURIComponent(
      subject
    )}&body=${encodeURIComponent(body)}`;
    showNotification("Email client opened!");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Notification */}
        {notification && (
          <div className="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-pulse">
            {notification}
          </div>
        )}

        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center">
                <Stethoscope className="w-8 h-8 text-white" />
              </div>
            </div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              Medical Report Generator Pro
            </h1>
            <p className="text-gray-600">
              Generate, view, export, and manage comprehensive medical reports
            </p>
          </div>

          {/* Control Buttons */}
          <div className="flex flex-wrap gap-3 justify-center">
            <Button
              onClick={generateMedicalReport}
              disabled={isGenerating}
              variant="primary"
              size="lg"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Generating...
                </>
              ) : (
                <>
                  <RefreshCw className="w-5 h-5" />
                  Generate New Report
                </>
              )}
            </Button>

            {medicalReport && (
              <>
                <Button
                  onClick={() => setShowPreviewModal(true)}
                  variant="secondary"
                >
                  <Eye className="w-5 h-5" />
                  Preview
                </Button>

                <Button onClick={handlePrint} variant="secondary">
                  <Printer className="w-5 h-5" />
                  Print
                </Button>

                <Button onClick={downloadAsJSON} variant="success">
                  <Download className="w-5 h-5" />
                  JSON
                </Button>

                <Button onClick={downloadAsCSV} variant="success">
                  <Download className="w-5 h-5" />
                  CSV
                </Button>

                <Button
                  onClick={() => setShowJsonModal(true)}
                  variant="secondary"
                >
                  <FileJson className="w-5 h-5" />
                  View JSON
                </Button>

                <Button onClick={copyToClipboard} variant="secondary">
                  <Copy className="w-5 h-5" />
                  Copy
                </Button>

                <Button onClick={shareReport} variant="secondary">
                  <Share2 className="w-5 h-5" />
                  Share
                </Button>

                <Button onClick={emailReport} variant="secondary">
                  <Mail className="w-5 h-5" />
                  Email
                </Button>

                <Button onClick={saveReport} variant="success">
                  <Save className="w-5 h-5" />
                  Save
                </Button>
              </>
            )}

            <Button
              onClick={() => setShowSavedReports(true)}
              variant="secondary"
              disabled={savedReports.length === 0}
            >
              <FileText className="w-5 h-5" />
              Saved Reports ({savedReports.length})
            </Button>
          </div>
        </div>

        {/* Medical Report Display */}
        {medicalReport && (
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div
              ref={reportRef}
              className="bg-white"
              style={{
                maxWidth: "210mm",
                minHeight: "297mm",
                margin: "0 auto",
                padding: "20mm",
                backgroundColor: "white",
              }}
            >
              {/* Hospital Header */}
              <div className="text-center py-8 border-b-2 border-indigo-200">
                <div className="flex justify-center mb-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-indigo-600 to-blue-600 rounded-full flex items-center justify-center">
                    <Activity className="w-6 h-6 text-white" />
                  </div>
                </div>
                <h2 className="text-3xl font-bold text-indigo-600 mb-2">
                  Evergreen Wellness Hospital
                </h2>
                <p className="text-gray-600 mb-4">
                  123 Harmony Street, Sunnyville, CA 90210, USA
                </p>
                <h1 className="text-4xl font-bold text-gray-800 bg-indigo-50 py-3 px-6 rounded-lg inline-block">
                  MEDICAL REPORT
                </h1>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
                {/* Left Column */}
                <div className="space-y-6">
                  {/* Visit Info */}
                  <div className="bg-indigo-50 p-6 rounded-lg">
                    <div className="flex items-center mb-4">
                      <User className="w-5 h-5 text-indigo-600 mr-2" />
                      <h3 className="text-lg font-semibold text-indigo-600">
                        Visit Information
                      </h3>
                    </div>
                    <div className="space-y-2 text-gray-700">
                      <p>
                        <span className="font-medium">Doctor:</span>{" "}
                        {medicalReport.doctorName}
                      </p>
                      <p>
                        <span className="font-medium">Specialty:</span>{" "}
                        {medicalReport.doctorSpecialty}
                      </p>
                      <p>
                        <span className="font-medium">Visit Date:</span>{" "}
                        {new Date(
                          medicalReport.reportDate
                        ).toLocaleDateString()}
                      </p>
                      <p>
                        <span className="font-medium">Follow-up:</span>{" "}
                        {new Date(
                          medicalReport.followUpDate
                        ).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  {/* Patient Info */}
                  <div className="bg-blue-50 p-6 rounded-lg">
                    <div className="flex items-center mb-4">
                      <User className="w-5 h-5 text-blue-600 mr-2" />
                      <h3 className="text-lg font-semibold text-blue-600">
                        Patient Information
                      </h3>
                    </div>
                    <div className="space-y-2 text-gray-700">
                      <p>
                        <span className="font-medium">Name:</span>{" "}
                        {medicalReport.patientName}
                      </p>
                      <p>
                        <span className="font-medium">ID:</span>{" "}
                        {medicalReport.patientId}
                      </p>
                      <p>
                        <span className="font-medium">DOB:</span>{" "}
                        {new Date(
                          medicalReport.dateOfBirth
                        ).toLocaleDateString()}
                      </p>
                      <p>
                        <span className="font-medium">Gender:</span>{" "}
                        {medicalReport.gender}
                      </p>
                      <p>
                        <span className="font-medium">Phone:</span>{" "}
                        {medicalReport.contactNumber}
                      </p>
                      <p>
                        <span className="font-medium">Email:</span>{" "}
                        {medicalReport.email}
                      </p>
                    </div>
                  </div>

                  {/* Vital Signs */}
                  <div className="bg-green-50 p-6 rounded-lg">
                    <div className="flex items-center mb-4">
                      <Activity className="w-5 h-5 text-green-600 mr-2" />
                      <h3 className="text-lg font-semibold text-green-600">
                        Vital Signs
                      </h3>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p>
                          <span className="font-medium">BP:</span>{" "}
                          {medicalReport.vitalSigns.bloodPressure} mmHg
                        </p>
                        <p>
                          <span className="font-medium">HR:</span>{" "}
                          {medicalReport.vitalSigns.heartRate} bpm
                        </p>
                        <p>
                          <span className="font-medium">Temp:</span>{" "}
                          {medicalReport.vitalSigns.temperature}°F
                        </p>
                        <p>
                          <span className="font-medium">RR:</span>{" "}
                          {medicalReport.vitalSigns.respiratoryRate}/min
                        </p>
                      </div>
                      <div>
                        <p>
                          <span className="font-medium">O2 Sat:</span>{" "}
                          {medicalReport.vitalSigns.oxygenSaturation}%
                        </p>
                        <p>
                          <span className="font-medium">Weight:</span>{" "}
                          {medicalReport.vitalSigns.weight} kg
                        </p>
                        <p>
                          <span className="font-medium">Height:</span>{" "}
                          {medicalReport.vitalSigns.height} cm
                        </p>
                        <p>
                          <span className="font-medium">BMI:</span>{" "}
                          {medicalReport.vitalSigns.bmi}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Right Column */}
                <div className="space-y-6">
                  {/* Lab Results */}
                  <div className="bg-purple-50 p-6 rounded-lg">
                    <div className="flex items-center mb-4">
                      <FileText className="w-5 h-5 text-purple-600 mr-2" />
                      <h3 className="text-lg font-semibold text-purple-600">
                        Lab Results
                      </h3>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p>
                          <span className="font-medium">Hgb:</span>{" "}
                          {medicalReport.labResults.hemoglobin} g/dL
                        </p>
                        <p>
                          <span className="font-medium">WBC:</span>{" "}
                          {medicalReport.labResults.whiteBloodCells.toLocaleString()}
                          /μL
                        </p>
                        <p>
                          <span className="font-medium">Platelets:</span>{" "}
                          {medicalReport.labResults.platelets.toLocaleString()}
                          /μL
                        </p>
                        <p>
                          <span className="font-medium">Glucose:</span>{" "}
                          {medicalReport.labResults.glucose} mg/dL
                        </p>
                      </div>
                      <div>
                        <p>
                          <span className="font-medium">Creatinine:</span>{" "}
                          {medicalReport.labResults.creatinine} mg/dL
                        </p>
                        <p>
                          <span className="font-medium">Cholesterol:</span>{" "}
                          {medicalReport.labResults.cholesterol} mg/dL
                        </p>
                        <p>
                          <span className="font-medium">Sodium:</span>{" "}
                          {medicalReport.labResults.sodium} mEq/L
                        </p>
                        <p>
                          <span className="font-medium">Potassium:</span>{" "}
                          {medicalReport.labResults.potassium} mEq/L
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Assessment & Diagnosis */}
                  <div className="bg-orange-50 p-6 rounded-lg">
                    <div className="flex items-center mb-4">
                      <Stethoscope className="w-5 h-5 text-orange-600 mr-2" />
                      <h3 className="text-lg font-semibold text-orange-600">
                        Assessment & Diagnosis
                      </h3>
                    </div>
                    <div className="space-y-3 text-gray-700">
                      <div>
                        <p className="font-medium text-orange-700 mb-1">
                          Clinical Notes:
                        </p>
                        <p className="text-sm leading-relaxed">
                          {medicalReport.medicalNotes}
                        </p>
                      </div>
                      <div>
                        <p className="font-medium text-orange-700 mb-1">
                          Primary Diagnosis:
                        </p>
                        <p className="text-sm leading-relaxed">
                          {medicalReport.diagnosis}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Treatment & Medications */}
                  <div className="bg-red-50 p-6 rounded-lg">
                    <div className="flex items-center mb-4">
                      <Pill className="w-5 h-5 text-red-600 mr-2" />
                      <h3 className="text-lg font-semibold text-red-600">
                        Treatment Plan
                      </h3>
                    </div>
                    <div className="space-y-3 text-gray-700">
                      <div>
                        <p className="font-medium text-red-700 mb-1">
                          Treatment:
                        </p>
                        <p className="text-sm leading-relaxed">
                          {medicalReport.treatment}
                        </p>
                      </div>
                      <div>
                        <p className="font-medium text-red-700 mb-1">
                          Medications:
                        </p>
                        <ul className="text-sm space-y-1">
                          {medicalReport.medications.map((med, index) => (
                            <li key={index} className="flex items-center">
                              <span className="w-2 h-2 bg-red-400 rounded-full mr-2"></span>
                              {med}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Footer */}
              <div className="bg-gradient-to-r from-indigo-50 to-blue-50 p-6 mt-8 rounded-lg border-t-4 border-indigo-600">
                <div className="text-center text-gray-600">
                  <p className="font-semibold mb-2">Contact Information</p>
                  <p className="text-sm">
                    Phone: +1 (555) 123-4567 | Email:
                    info@EvergreenWellnessHospital.com
                  </p>
                  <p className="text-sm">www.EvergreenWellnessHospital.com</p>
                  <p className="text-xs mt-3 text-gray-500">
                    This report is confidential and intended for medical
                    professionals only.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* JSON Modal */}
        <Modal
          size="xl"
          title="Medical Report JSON Data"
          isOpen={showJsonModal}
          onClose={() => setShowJsonModal(false)}
        >
          <div className="space-y-4">
            <div className="flex gap-2 mb-4">
              <Button onClick={copyToClipboard} size="sm">
                <Copy className="w-4 h-4" />
                Copy JSON
              </Button>
              <Button onClick={downloadAsJSON} variant="success" size="sm">
                <Download className="w-4 h-4" />
                Download JSON
              </Button>
            </div>
            <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-sm font-mono max-h-96">
              {JSON.stringify(medicalReport, null, 2)}
            </pre>
          </div>
        </Modal>

        {/* Preview Modal */}
        <Modal
          size="xl"
          title="Report Preview"
          isOpen={showPreviewModal}
          onClose={() => setShowPreviewModal(false)}
        >
          <div className="space-y-4">
            <div className="flex gap-2 mb-4">
              <Button onClick={handlePrint} size="sm">
                <Printer className="w-4 h-4" />
                Print
              </Button>
              <Button onClick={downloadAsJSON} variant="success" size="sm">
                <Download className="w-4 h-4" />
                Download
              </Button>
              <Button onClick={shareReport} variant="secondary" size="sm">
                <Share2 className="w-4 h-4" />
                Share
              </Button>
            </div>
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
                  <h1 className="text-3xl font-bold text-gray-800">
                    MEDICAL REPORT
                  </h1>
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
                        {medicalReport.reportDate
                          .split("-")
                          .reverse()
                          .join(".")}
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
                          {medicalReport.dateOfBirth
                            .split("-")
                            .reverse()
                            .join(".")}
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
                      {medicalReport.patientName.split(" ")[1]} appears in good
                      health with no immediate concerns during the examination.
                      Based on the assessment, there are no significant issues
                      detected, and vital signs are within normal ranges.
                    </p>
                  </div>

                  {/* Diagnosis */}
                  <div>
                    <h3 className="text-lg font-semibold text-green-600 mb-3">
                      Diagnosis
                    </h3>
                    <p className="text-gray-700 leading-relaxed">
                      After thorough examination,{" "}
                      {medicalReport.diagnosis.toLowerCase()}. The diagnosis
                      indicates a healthy status with no evidence of underlying
                      health issues.
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
            {/* {medicalReport && (
              <div className="border rounded-lg p-4 bg-gray-50 max-h-96 overflow-y-auto">
                <div className="bg-white p-6 rounded-lg shadow-sm">
                  <div className="text-center border-b pb-4 mb-4">
                    <h2 className="text-xl font-bold text-indigo-600">Evergreen Wellness Hospital</h2>
                    <p className="text-sm text-gray-600">Medical Report Summary</p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <h3 className="font-semibold text-indigo-600 mb-2">Patient Info</h3>
                      <p><strong>Name:</strong> {medicalReport.patientName}</p>
                      <p><strong>ID:</strong> {medicalReport.patientId}</p>
                      <p><strong>DOB:</strong> {new Date(medicalReport.dateOfBirth).toLocaleDateString()}</p>
                      <p><strong>Gender:</strong> {medicalReport.gender}</p>
                    </div>
                    <div>
                      <h3 className="font-semibold text-indigo-600 mb-2">Visit Info</h3>
                      <p><strong>Doctor:</strong> {medicalReport.doctorName}</p>
                      <p><strong>Specialty:</strong> {medicalReport.doctorSpecialty}</p>
                      <p><strong>Date:</strong> {new Date(medicalReport.reportDate).toLocaleDateString()}</p>
                    </div>
                  </div>
                  
                  <div className="mt-4">
                    <h3 className="font-semibold text-indigo-600 mb-2">Diagnosis</h3>
                    <p className="text-sm bg-blue-50 p-3 rounded">{medicalReport.diagnosis}</p>
                  </div>
                  
                  <div className="mt-4">
                    <h3 className="font-semibold text-indigo-600 mb-2">Treatment</h3>
                    <p className="text-sm bg-green-50 p-3 rounded">{medicalReport.treatment}</p>
                  </div>
                </div>
              </div>
            )} */}
          </div>
        </Modal>

        {/* Saved Reports Modal */}
        <Modal
          size="xl"
          title="Saved Medical Reports"
          isOpen={showSavedReports}
          onClose={() => setShowSavedReports(false)}
        >
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold">
                Saved Reports ({savedReports.length})
              </h3>
              {savedReports.length > 0 && (
                <Button onClick={clearAllReports} variant="danger" size="sm">
                  <FileX className="w-4 h-4" />
                  Clear All
                </Button>
              )}
            </div>

            {savedReports.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <FileText className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No saved reports yet</p>
                <p className="text-sm">
                  Generate and save reports to access them here
                </p>
              </div>
            ) : (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {savedReports.map((report, index) => (
                  <div
                    key={index}
                    className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-800">
                          {report.patientName}
                        </h4>
                        <p className="text-sm text-gray-600">
                          ID: {report.patientId}
                        </p>
                        <p className="text-sm text-gray-600">
                          Date:{" "}
                          {new Date(report.reportDate).toLocaleDateString()}
                        </p>
                        <p className="text-sm text-gray-600">
                          Doctor: {report.doctorName}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {report.diagnosis}
                        </p>
                      </div>
                      <div className="flex gap-2 ml-4">
                        <Button
                          onClick={() => loadSavedReport(report)}
                          variant="primary"
                          size="sm"
                        >
                          Load
                        </Button>
                        <Button
                          onClick={() => deleteSavedReport(index)}
                          variant="danger"
                          size="sm"
                        >
                          Delete
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </Modal>

        {/* Statistics Card */}
        {medicalReport && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mt-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Report Statistics
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <User className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-blue-600">1</div>
                <div className="text-sm text-gray-600">Active Patient</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <Activity className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-green-600">8</div>
                <div className="text-sm text-gray-600">Vital Signs</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <FileText className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-purple-600">8</div>
                <div className="text-sm text-gray-600">Lab Results</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <Pill className="w-8 h-8 text-orange-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-orange-600">
                  {medicalReport.medications.length}
                </div>
                <div className="text-sm text-gray-600">Medications</div>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-8 text-gray-600">
          <p className="text-sm">
            Medical Report Generator Pro - Advanced healthcare documentation
            system
          </p>
          <p className="text-xs mt-2">
            Generate, export, and manage comprehensive medical reports with ease
          </p>
        </div>
      </div>
    </div>
  );
};
export default CreateDataPage;
