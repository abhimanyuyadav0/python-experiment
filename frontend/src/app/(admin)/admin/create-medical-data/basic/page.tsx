"use client";

import Modal from "@/components/modal";
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

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
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
              View JSON Data
            </button>
          </div>

          {medicalReport && (
            <div className="bg-gray-50 rounded-lg p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                Generated Medical Report
              </h2>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Patient Information */}
                <div className="bg-white p-4 rounded-lg shadow">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">
                    Patient Information
                  </h3>
                  <div className="space-y-2 text-sm">
                    <p>
                      <span className="font-medium">Patient ID:</span>{" "}
                      {medicalReport.patientId}
                    </p>
                    <p>
                      <span className="font-medium">Name:</span>{" "}
                      {medicalReport.patientName}
                    </p>
                    <p>
                      <span className="font-medium">Date of Birth:</span>{" "}
                      {medicalReport.dateOfBirth}
                    </p>
                    <p>
                      <span className="font-medium">Gender:</span>{" "}
                      {medicalReport.gender}
                    </p>
                    <p>
                      <span className="font-medium">Contact:</span>{" "}
                      {medicalReport.contactNumber}
                    </p>
                    <p>
                      <span className="font-medium">Email:</span>{" "}
                      {medicalReport.email}
                    </p>
                    <p>
                      <span className="font-medium">Address:</span>{" "}
                      {medicalReport.address}
                    </p>
                  </div>
                </div>

                {/* Vital Signs */}
                <div className="bg-white p-4 rounded-lg shadow">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">
                    Vital Signs
                  </h3>
                  <div className="space-y-2 text-sm">
                    <p>
                      <span className="font-medium">Blood Pressure:</span>{" "}
                      {medicalReport.vitalSigns.bloodPressure} mmHg
                    </p>
                    <p>
                      <span className="font-medium">Heart Rate:</span>{" "}
                      {medicalReport.vitalSigns.heartRate} bpm
                    </p>
                    <p>
                      <span className="font-medium">Temperature:</span>{" "}
                      {medicalReport.vitalSigns.temperature}°F
                    </p>
                    <p>
                      <span className="font-medium">Respiratory Rate:</span>{" "}
                      {medicalReport.vitalSigns.respiratoryRate} breaths/min
                    </p>
                    <p>
                      <span className="font-medium">Oxygen Saturation:</span>{" "}
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

                {/* Lab Results */}
                <div className="bg-white p-4 rounded-lg shadow">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">
                    Laboratory Results
                  </h3>
                  <div className="space-y-2 text-sm">
                    <p>
                      <span className="font-medium">Hemoglobin:</span>{" "}
                      {medicalReport.labResults.hemoglobin} g/dL
                    </p>
                    <p>
                      <span className="font-medium">White Blood Cells:</span>{" "}
                      {medicalReport.labResults.whiteBloodCells.toLocaleString()}{" "}
                      /μL
                    </p>
                    <p>
                      <span className="font-medium">Platelets:</span>{" "}
                      {medicalReport.labResults.platelets.toLocaleString()} /μL
                    </p>
                    <p>
                      <span className="font-medium">Glucose:</span>{" "}
                      {medicalReport.labResults.glucose} mg/dL
                    </p>
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

                {/* Medical Information */}
                <div className="bg-white p-4 rounded-lg shadow">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">
                    Medical Information
                  </h3>
                  <div className="space-y-3 text-sm">
                    <div>
                      <span className="font-medium">Diagnosis:</span>
                      <p className="mt-1 text-gray-600">
                        {medicalReport.diagnosis}
                      </p>
                    </div>
                    <div>
                      <span className="font-medium">Treatment:</span>
                      <p className="mt-1 text-gray-600">
                        {medicalReport.treatment}
                      </p>
                    </div>
                    <div>
                      <span className="font-medium">Medical Notes:</span>
                      <p className="mt-1 text-gray-600">
                        {medicalReport.medicalNotes}
                      </p>
                    </div>
                    <div>
                      <span className="font-medium">Medications:</span>
                      <ul className="mt-1 text-gray-600 list-disc list-inside">
                        {medicalReport.medications.map((med, index) => (
                          <li key={index}>{med}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Doctor Information */}
                <div className="bg-white p-4 rounded-lg shadow lg:col-span-2">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">
                    Doctor Information
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="font-medium">Doctor:</span>{" "}
                      {medicalReport.doctorName}
                    </div>
                    <div>
                      <span className="font-medium">Specialty:</span>{" "}
                      {medicalReport.doctorSpecialty}
                    </div>
                    <div>
                      <span className="font-medium">Follow-up Date:</span>{" "}
                      {medicalReport.followUpDate}
                    </div>
                    <div>
                      <span className="font-medium">Report Date:</span>{" "}
                      {medicalReport.reportDate}
                    </div>
                  </div>
                </div>
              </div>

              {/* JSON Export */}
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
          )}
        </div>
      </div>
    </div>
  );
};

export default CreateDataPage;
