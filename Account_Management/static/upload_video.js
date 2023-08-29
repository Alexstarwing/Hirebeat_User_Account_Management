function showLoading() {
    document.getElementById("loading").style.display = "block";
}

function hideLoading() {
    document.getElementById("loading").style.display = "none";
}

//paste here your copied configuration code
const firebaseConfig = {
    apiKey: "AIzaSyBxYu2sNjLgQsJJ7PwyK228DDdgg4rgSTw",
    authDomain: "hirebeat-561be.firebaseapp.com",
    projectId: "hirebeat-561be",
    storageBucket: "hirebeat-561be.appspot.com",
    messagingSenderId: "100708272950",
    appId: "1:100708272950:web:7fbab5c81409113efd8197",
    measurementId: "G-56Z0DL0SH3"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

function uploadVideo() {
    showLoading();

    const ref = firebase.storage().ref();
    const file = document.querySelector("#choose_file").files[0];
    const name = +new Date() + "-" + file.name;
    const metadata = {
     contentType: file.type
    };
    const task = ref.child('video/account/' + name).put(file, metadata);
    task.then(snapshot => snapshot.ref.getDownloadURL())
    .then(url => {
      console.log(url);
      alert('Video uploaded successfully');
      document.querySelector("#video").src = url;

      getDownloadURLForVideo('video/account/' + name);
      hideLoading();
    })
    .catch(console.error);
}

function getDownloadURLForVideo(VideoPath) {
  const storageRef = firebase.storage().ref();
  const videoRef = storageRef.child(VideoPath);
  let video_url = document.querySelector('input[name="video_url"]');
  videoRef.getDownloadURL()
      .then((url) => {
         console.log("Video URL:", url);
         document.querySelector("#video").src = url;
         video_url.value = url;
      })
      .catch((error) => {
         console.error("Error getting download URL:", error);
      });
}