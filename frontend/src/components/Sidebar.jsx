import React, {useState} from 'react';
import { Link } from 'react-router-dom';

import {
    LuBox,
} from 'react-icons/lu';
import {
    MdTableView,
    MdOutlineNewspaper,
} from 'react-icons/md';
import {
    FaSuitcase,
    FaFileUpload,
    FaTable
} from 'react-icons/fa';
import {
    TbUsers,
    TbHelpHexagon,
} from 'react-icons/tb';

const Sidebar = () => {
    const [activeLink, setActiveLink] = useState(0);

    const SIDEBAR_LINKS = [
        {id:1, path: '/', name:"Dashboard", icon:LuBox},
        {id:2, path: '/users', name:"Users", icon:TbUsers},
        {id:3, path: '/open-orders', name:"Open Orders", icon:FaSuitcase},
        {id:4, path: '/upload-images', name:"Upload Images", icon:FaFileUpload},
        {id:5, path: '/gangsheets', name:"Gangsheets", icon:FaTable},
        {id:6, path: '/missing-images', name:"Missing Items", icon:MdTableView},
        {id:7, path: '/gangsheet-builder-poc', name:"Gangsheet Builder POC", icon:MdOutlineNewspaper},
    ];

    const handleLinkClick = (index) => {
        setActiveLink(index)
    }
    return (
        <div className='w-16 md:w-56 fixed left-0 top-0 z-10 h-screen border-r pt-8 px-4 bg-white'>
            {/* logo */}
            <div className="mb-8 flex justify-center">
                <img src="/PT_Logo_W_Text.svg" alt='logo' className='w-36 hidden md:flex' />
                <img src="/PT_Logo.svg" alt='logo' className='w-8 flex md:hidden' />
            </div>

            {/* nav links */}
            <ul className="mt-6 space-y-6">
                {
                    SIDEBAR_LINKS.map((link, index) => (
                        <li 
                            key={`sidebar ${index}`} 
                            className={`font-medium rounded-md py-2 px-5 hover:bg-gray-100 hover:text-indigo-500 ${activeLink === index ? 'bg-indigo-100 text-indigo-500' : ''}`}
                        >
                            <Link 
                                to={link.path} 
                                className='flex justify-center md:justify-start items-center md:space-x-5'
                                onClick={() => handleLinkClick(index)}
                            >
                                <span>{link.icon()}</span>
                                <span className="text-sm text-gray-500 hidden md:flex">{link.name}</span>
                            </Link>
                        </li>
                    ))
                }
            </ul>

            {/* need help */}
            <div className="w-full absolute bottom-5 left-0 px-4 py-2 cursor-pointer text-center">
                <p className="flex items-center space-x-2 text-xs text-white py-2 px-5 bg-gradient-to-r from-indigo-500 to-violet-600 rounded-full justify-center">
                    <span><TbHelpHexagon size={28} /></span><span className="text-center mr-auto ml-auto hidden md:flex">Need Help?<br />Ask a Panda!</span>
                </p>
            </div>
        </div>
    )
};

export default Sidebar;