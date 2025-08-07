import axoisInstance from "../../axois";
interface UploadOptions{
  onProgress?: (progress: number) => void;
  onComplete?: (result: any) => void;
  onError?: (error: any) => void;
}

export const uploadFile = (file: File, options: UploadOptions) => {
  return new Promise<string>((resolve) => {
    const totalDuration = 120000; // 2 minutes in milliseconds
    const intervalTime = 1000; // update every 1 second
    let elapsed = 0;

    const interval = setInterval(() => {
      elapsed += intervalTime;
      const percent = Math.min((elapsed / totalDuration) * 100, 100);

      if (options?.onProgress) {
        options.onProgress(Math.round(percent));
      }

      if (elapsed >= totalDuration) {
        clearInterval(interval);
        // Return dummy URL
        resolve(`https://dummyserver.com/uploads/${file.name}`);
      }
    }, intervalTime);
  });
};
