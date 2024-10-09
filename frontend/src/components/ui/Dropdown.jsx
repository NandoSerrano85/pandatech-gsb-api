import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import PropTypes from 'prop-types';

import { isEmpty } from '@/utils';

const Dropdown = (props) => {
    const {
        dropdownName,
        dropdownItems,
        onshow,
        visible,
        classname,
        icon,
    } = props;

    const menuItemBuilder = (data) => {
        if (!isEmpty(data)) {
            return data.map((item, index) => {
                return (
                    <> 
                        {item.lineBefore && (
                            <hr className="py-1" />
                        )}
                        {!item.isInput && (
                            <MenuItem key={`dropdown-menu-item-${index}`} onClick={item.onclick()}>
                            <a
                                href={item.link}
                                className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100 data-[focus]:text-gray-900"
                            >
                                {item.itemName}
                            </a>
                        </MenuItem>
                        )}
                        {item.isInput && (
                            <MenuItem key={`dropdown-menu-item-${index}`} onClick={item.onclick()}>
                            <label
                                className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100 data-[focus]:text-gray-900"
                            >
                                {item.itemName}
                            </label>
                            <input
                                id={item.itemInput.id}
                                type={item.itemInput.type}
                                min={item.itemInput.min}
                                max={item.itemInput.max}
                                onChange={(e) => item.itemInput.onChange(e)}
                            />
                        </MenuItem>
                        )}
                    </>
                )
            })
        }
    }
  return (
    <Menu as="div" className={`relative inline-block text-left ${classname}`}>
      <div>
        <MenuButton 
            className="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" 
            onShow={() => onshow()}
        >
          <span>{icon}</span>
          <span className="hidden md:flex">{dropdownName}</span>
        </MenuButton>
      </div>

        {visible &&(
            <MenuItems
                transition
                className="absolute right-0 z-10 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
            >
                {menuItemBuilder(dropdownItems)}
          </MenuItems>
        )}
    </Menu>
  )
}
Dropdown.defaultProps = {
    dropdownName: '',
    classname: '',
    onshow: () => {},
    visible: true,
    dropdownItems: [{
        itemName: '',
        link: '',
        lineBefore: false,
        onclick: () => {},
        itemIcon: null,
        isInput: false,
        itemInput: {
            min: 0,
            max: 0,
            type: '',
            id: '',
            onChange: () =>{},
        },
    }],
}

Dropdown.propTypes = {
    dropdownName: PropTypes.string,
    dropdownItems: PropTypes.arrayOf(PropTypes.shape({
        itemName: PropTypes.string,
        link: PropTypes.string,
        lineBefore: PropTypes.bool,
        onclick: PropTypes.func,
        itemIcon: PropTypes.node,
        isInput: PropTypes.bool,
        itemInput: PropTypes.shape({
            min: PropTypes.number,
            max: PropTypes.number,
            type: PropTypes.string,
            id: PropTypes.string,
            onChange: PropTypes.func,
        }),
    })),
    classname: PropTypes.string,
    visible: PropTypes.bool,
    onshow: PropTypes.func,
    icon: PropTypes.node,
};

export default Dropdown;