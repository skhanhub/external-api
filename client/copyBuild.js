const fs = require('fs-extra');

// copy source folder to destination
fs.copy('./build', '../server/static', function (err) {
  if (err) {
    console.log('An error occured while copying the folder.');
    return console.error(err);
  }
  console.log('Copy completed!');
});
