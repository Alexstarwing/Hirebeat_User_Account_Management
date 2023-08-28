
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
    console.log(firebase);

    function uploadImage() {
        const ref = firebase.storage().ref();
        const file = document.querySelector("#photo").files[0];
        const accountName = document.getElementById("accountName").value;
        const metadata = {
         contentType: file.type
        };
        const task = ref.child("logo/account/" + accountName).put(file, metadata);
        task.then(snapshot => snapshot.ref.getDownloadURL())
              .then(url => {
                 console.log(url);
                 alert('image uploaded successfully');
                 document.querySelector("#image").src = url;


                 getDownloadURLForImage("logo/account/" + accountName);
              })
              .catch(console.error);
   }

    function getDownloadURLForImage(imagePath) {
      const storageRef = firebase.storage().ref();
      const imageRef = storageRef.child(imagePath);
      var profileLogoInput = document.querySelector('input[name="profile_logo"]');

      imageRef.getDownloadURL()
          .then((url) => {
             console.log("Image URL:", url);
             document.querySelector("#image").src = url;
             profileLogoInput.value = url;
          })
          .catch((error) => {
             console.error("Error getting download URL:", error);
          });
   }