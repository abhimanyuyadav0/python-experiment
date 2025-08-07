"use client";

import Modal from "@/components/modal";
import { FileJson, FileText, XIcon } from "lucide-react";
import React, { useState } from "react";

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

  const generateRandomName = () => {
    const firstNames = [
      "John",
      "Jane",
      "Michael",
      "Sarah",
      "David",
      "Emily",
      "Robert",
      "Lisa",
      "James",
      "Maria",
      "William",
      "Jennifer",
      "Richard",
      "Linda",
      "Thomas",
      "Patricia",
      "Christopher",
      "Barbara",
      "Daniel",
      "Elizabeth",
    ];
    const lastNames = [
      "Smith",
      "Johnson",
      "Williams",
      "Brown",
      "Jones",
      "Garcia",
      "Miller",
      "Davis",
      "Rodriguez",
      "Martinez",
      "Hernandez",
      "Lopez",
      "Gonzalez",
      "Wilson",
      "Anderson",
      "Thomas",
      "Taylor",
      "Moore",
      "Jackson",
      "Martin",
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

  const handlePrintPdf = () => {
    console.log("Printing PDF");
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Medical Report Data Generator
      </h1>

      <div className="flex gap-4 mb-8">
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
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center gap-2"
          onClick={() => {
            handlePrintPdf();
          }}
        >
          <FileText /> Print PDF
        </button>
      </div>

      {medicalReport && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
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

          <div className="p-8 space-y-6">
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
          <div className="bg-gray-50 px-8 py-6 border-t border-gray-200">
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
    </div>
  );
};

export default CreateDataPage;
