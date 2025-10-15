"use client";

import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload } from "lucide-react";
import Link from "next/link";
import Image from "next/image";
export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [reverbType, setReverbType] = useState("simple");

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    multiple: false,
    accept: { "audio/wav": [".wav"] },
    onDrop: (acceptedFiles) => {
      if (acceptedFiles && acceptedFiles[0]) {
        setSelectedFile(acceptedFiles[0]);
      }
    },
  });

  const handleApplyReverb = async () => {
    if (!selectedFile) {
      alert("Please select a WAV file first.");
      return;
    }

    setIsProcessing(true);

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("reverb_type", reverbType);

    try {
      const response = await fetch("http://127.0.0.1:8000/apply_reverb/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`Request failed: ${response.status}`);

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${selectedFile.name.replace(
        ".wav",
        ""
      )}_${reverbType}_reverb.wav`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      alert("Reverb applied successfully!");
      setSelectedFile(null);
    } catch (err) {
      console.error(err);
      alert("Failed to apply reverb. Please try again.");
    }

    setIsProcessing(false);
  };

  return (
    <div className="flex flex-col min-h-screen font-sans bg-gradient-to-b from-blue-50 to-green-50">
      <main className="flex-grow flex flex-col items-center mx-20">
        <header className="flex justify-center p-4">
          <Link
            href="https://craigo.live/"
            target="_blank"
            rel="noopener noreferrer"
            className="m-10 drop-shadow-lg/40"
          >
            <Image
              className="justify-items-center"
              src="/logo.png"
              alt="Craig Logo"
              width={100}
              height={100}
              priority
            />
          </Link>
        </header>

        <div className="flex flex-col items-center gap-4 bg-white border border-neutral-400 rounded-xl py-10 px-10 max-w-150 drop-shadow-xl">
          <h1 className="text-3xl font-bold text-center">Reverber</h1>
          <p>Reverberize your favorite .wav files!</p>

          <label className="mt-2">
            Select Reverb Type:
            <select
              value={reverbType}
              onChange={(e) => setReverbType(e.target.value)}
              className="ml-2 border rounded px-2 py-1"
            >
              <option value="simple">Simple</option>
              {/* <option value="comb">Comb</option>
              <option value="allpass">Allpass</option> */}
              <option value="schroeder">Schroeder</option>
              <option value="rir">RIR</option>
            </select>
          </label>

          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-2xl p-10 w-full flex flex-col items-center justify-center gap-3 cursor-pointer transition-colors ${
              isDragActive
                ? "border-green-500 bg-green-50"
                : "border-neutral-300"
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="w-12 h-12 text-green-500" />
            <p className="text-center">
              {selectedFile
                ? `Uploaded: ${selectedFile.name}`
                : "Drag and drop your .wav file here, or click to select"}
            </p>
          </div>

          <button
            className={`px-4 py-2 border rounded-full bg-blue-300 border-blue-500 hover:bg-blue-400 transition-colors duration-150 font-bold text-blue-800 ${
              !selectedFile || isProcessing
                ? "opacity-50 cursor-not-allowed"
                : ""
            }`}
            disabled={!selectedFile || isProcessing}
            onClick={handleApplyReverb}
          >
            {isProcessing ? "Processing..." : "Apply Reverb"}
          </button>
        </div>
      </main>

      <footer className="flex justify-center items-center p-4 border-t border-neutral-300">
        <p className="text-sm text-neutral-600">
          Created by <a className="text-blue-700">Craig Ondevilla</a>
        </p>
      </footer>
    </div>
  );
}
