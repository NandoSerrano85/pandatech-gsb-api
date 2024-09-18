import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import { Outlet } from 'react-router-dom';

const Layout = () => {
    const username = "Fernie"
    const image = {
        path: "https://media.licdn.com/dms/image/v2/C4E03AQHADSq7jnzwMg/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1588108525675?e=1731542400&v=beta&t=Ro0grXJhk1xpWfQNKq15A4VEBV83jYP2ALK4GLxR8jE",
        alt: "profile image"
    }
    return (
        <div className="flex">
            <Sidebar />
            <div className="w-full ml-16 md:ml-56">
                <Header username={username} image={image} />
                <div className="px-2 py-2">
                    <Outlet />
                </div>
            </div>
        </div>
    )
}

export default Layout;