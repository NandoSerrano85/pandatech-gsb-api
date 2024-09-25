import {
  BrowserRouter as Router,
  Route,
  Routes,
} from 'react-router-dom';
import { Layout } from './components';
import {
  Home,
  OpenOrders,
  Users,
  UploadImages,
  Gangsheets,
  MissingImages,
  Profile,
  GangsheetBuilderPOC,
  Products,
 } from './pages';
const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="users" element={<Users />} />
          <Route path="open-orders" element={<OpenOrders />} />
          <Route path="products" element={<Products />} />
          <Route path="upload-images" element={<UploadImages />} />
          <Route path="gangsheets" element={<Gangsheets />} />
          <Route path="missing-images" element={<MissingImages />} />
          <Route path="profile" element={<Profile />} />
          <Route path="gangsheet-builder-poc" element={<GangsheetBuilderPOC />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App;
