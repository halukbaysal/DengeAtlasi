const fs = require('node:fs');
const path = require('node:path');

const buildFile = path.join(
  __dirname,
  '..',
  'node_modules',
  'react-native-tts',
  'android',
  'build.gradle',
);

if (fs.existsSync(buildFile)) {
  const original = fs.readFileSync(buildFile, 'utf8');
  const legacyBuildscript = `buildscript {
    repositories {
        jcenter()
    }

    dependencies {
        classpath 'com.android.tools.build:gradle:1.3.1'
    }
}

`;
  let patched = original.replace(legacyBuildscript, '');
  if (!patched.includes('namespace "net.no_mad.tts"')) {
    patched = patched.replace(
      'android {\n',
      'android {\n    namespace "net.no_mad.tts"\n',
    );
  }
  if (patched === original && original.includes('jcenter()')) {
    throw new Error('react-native-tts Android compatibility patch did not apply.');
  }
  fs.writeFileSync(buildFile, patched);
}
