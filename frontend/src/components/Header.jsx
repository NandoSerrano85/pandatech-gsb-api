import PropTypes from 'prop-types';
import { GoBell } from 'react-icons/go';
import { Link } from 'react-router-dom';

const Header = (props) => {
    const {
        username,
        image,
    } = props;

    return (
        <div className="flex justify-between items-center p-4">
            <div>
                <h1 className="text-xs">Welcome Back!</h1>
                <p className="text-xl font-semibold">{username}</p>
            </div>
            <div className='flex items-center space-x-5'>
                <div className='hidden md:flex'>
                    <input className='bg-indigo-100/30 px-4 py-2 rounded-lg focus:ring-2 focus:ring-indigo-600' type="text" placeholder="Search ..." />
                </div>
                <div className='flex items-center space-x-5'>
                    <button className='relative text-2x1 text-gray-600'>
                        <GoBell size={28} />
                        <span className='absolute top-0 right-0 -mt-1 -mr-1 flex justify-center bg-indigo-600 text-white font-semibold text-[10px] w-5 h-4 rounded-full border-2 border-white'>9</span>
                    </button>
                    <Link 
                        to={'/profile'} 
                    >
                        <img 
                            className='w-8 g-8 rounded-full border-2 border-indigo-400'
                            src={image.path} 
                            alt={image.alt} 
                        />
                    </Link>
                </div>
            </div>
        </div>
    )
};

Header.propTypes = {
    username: PropTypes.string.isRequired,
    image: PropTypes.shape({
        path: PropTypes.string,
        alt:PropTypes.string,
    }),
};

export default Header;