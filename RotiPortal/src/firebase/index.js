import { initializeApp } from "firebase/app"
import { getFirestore, collection, doc, setDoc, getDoc } from "firebase/firestore"
import { getAnalytics } from "firebase/analytics"
import { getAuth } from "firebase/auth"
import { getStorage } from 'firebase/storage';

const apiKey = import.meta.env.VITE_FIREBASE_apiKey
const authDomain = import.meta.env.VITE_FIREBASE_authDomain
const projectId = import.meta.env.VITE_FIREBASE_projectId
const storageBucket = import.meta.env.VITE_FIREBASE_storageBucket
const messagingSenderId = import.meta.env.VITE_FIREBASE_messagingSenderId
const appId = import.meta.env.VITE_FIREBASE_appId
const measurementId = import.meta.env.VITE_FIREBASE_measurementId

const firebaseConfig = {
  apiKey,
  authDomain,
  projectId,
  storageBucket,
  messagingSenderId,
  appId,
  measurementId,
}

const app = initializeApp(firebaseConfig)
export const firebase_firestore = getFirestore(app)
export const firebase_analytics = getAnalytics(app)
export const firebase_auth = getAuth(app)
export const firebase_storage = getStorage(app);
