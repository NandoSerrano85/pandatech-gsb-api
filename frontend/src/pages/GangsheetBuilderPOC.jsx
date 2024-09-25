import { useState, useRef, useEffect } from "react";
import {
  CDropdown as Dropdown,
  CDropdownToggle as DropdownToggle,
  CDropdownMenu as DropdownMenu,
  CDropdownItem as DropdownItem,
  CDropdownDivider as DropdownDivider,
} from '@coreui/react';
import { 
  MenuIcon,
  RefreshCwIcon,
  UndoIcon,
  RedoIcon,
  PlusIcon,
  ShareIcon,
  FlipHorizontalIcon,
  FlipVerticalIcon,
  SaveIcon,
  DownloadIcon 
} from "lucide-react";
import { useGesture } from '@use-gesture/react';

const GangsheetBuilderPOC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [fileMenuOpen, setFileMenuOpen] = useState(false);
  const [resizeMenuOpen, setResizeMenuOpen] = useState(false);
  const [images, setImages] = useState([])
  const [canvasSize, setCanvasSize] = useState({ width: 800, height: 600 })
  const [dpi, setDpi] = useState(300)
  const [canvasImages, setCanvasImages] = useState([])
  const [selectedImage, setSelectedImage] = useState(null)
  const [history, setHistory] = useState([])
  const [historyIndex, setHistoryIndex] = useState(-1)
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const canvasRef = useRef(null)
  const containerRef = useRef(null)
  const fileinputRef = useRef(null)

  useEffect(() => {
    drawCanvas()
    // fitCanvasToContainer()
  }, [canvasImages, zoom, pan])

  useEffect(() => {
    if (historyIndex >= 0) {
      setCanvasImages(history[historyIndex])
    }
  }, [historyIndex, history])

  useEffect(() => {
    window.addEventListener('resize', fitCanvasToContainer)
    return () => window.removeEventListener('resize', fitCanvasToContainer)
  }, [])

  const fitCanvasToContainer = () => {
    if (containerRef.current && canvasRef.current) {
      const containerWidth = containerRef.current.clientWidth
      const containerHeight = containerRef.current.clientHeight
      const canvasAspectRatio = canvasSize.width / canvasSize.height
      const containerAspectRatio = containerWidth / containerHeight

      let newZoom
      if (canvasAspectRatio > containerAspectRatio) {
        newZoom = containerWidth / canvasSize.width
      } else {
        newZoom = containerHeight / canvasSize.height
      }

      setZoom(newZoom * 0.9) // 90% to leave some margin
      setPan({ x: 0, y: 0 })
    }
  }

  const drawCanvas = () => {
    const canvas = canvasRef.current
    const ctx = canvas?.getContext('2d')
    if (ctx) {
      ctx.save()
      ctx.clearRect(0, 0, canvasSize.width, canvasSize.height)
      ctx.fillStyle = 'white'
      ctx.fillRect(0, 0, canvasSize.width, canvasSize.height)
      
      ctx.translate(pan.x, pan.y)
      ctx.scale(zoom, zoom)

      canvasImages.forEach(img => {
        const image = new Image()
        image.src = img.src
        ctx.save()
        ctx.translate(img.x + img.width / 2, img.y + img.height / 2)
        ctx.rotate((img.rotation * Math.PI) / 180)
        ctx.scale(img.flipX ? -1 : 1, img.flipY ? -1 : 1)
        ctx.drawImage(image, -img.width / 2, -img.height / 2, img.width, img.height)
        ctx.restore()
      })
      
      ctx.restore()
    }
  }

  const handleFileChange = (event) => {
    const files = event.target.files
    if (files) {
      const newImages = Array.from(files)
        .filter(file => file.type === "image/png")
        .map(file => URL.createObjectURL(file))
      setImages(prevImages => [...prevImages, ...newImages])
    }
  }

  const handleImageDoubleClick = (imageSrc) => {
    const img = new Image()
    img.onload = () => {
      const newImage = {
        id: Date.now().toString(),
        src: imageSrc,
        x: 0,
        y: 0,
        width: img.width,
        height: img.height,
        rotation: 0,
        flipX: false,
        flipY: false
      }
      addToHistory([...canvasImages, newImage])
    }
    img.src = imageSrc
  }

  const handleCanvasClick = (event) => {
    const canvas = canvasRef.current
    if (canvas) {
      const rect = canvas.getBoundingClientRect()
      const x = (event.clientX - rect.left - pan.x) / zoom
      const y = (event.clientY - rect.top - pan.y) / zoom
      const clickedImage = canvasImages.find(img => 
        x >= img.x && x <= img.x + img.width &&
        y >= img.y && y <= img.y + img.height
      )
      setSelectedImage(clickedImage || null)
    }
  }

  const updateSelectedImage = (updates) => {
    if (selectedImage) {
      const updatedImages = canvasImages.map(img => 
        img.id === selectedImage.id ? { ...img, ...updates } : img
      )
      addToHistory(updatedImages)
    }
  }

  const duplicateSelectedImage = () => {
    if (selectedImage) {
      const newImage = { ...selectedImage, id: Date.now().toString(), x: selectedImage.x + 20, y: selectedImage.y + 20 }
      addToHistory([...canvasImages, newImage])
    }
  }

  const addToHistory = (newState) => {
    setHistory(prevHistory => [...prevHistory.slice(0, historyIndex + 1), newState])
    setHistoryIndex(prevIndex => prevIndex + 1)
    setCanvasImages(newState)
  }

  const undo = () => {
    if (historyIndex > 0) {
      setHistoryIndex(prevIndex => prevIndex - 1)
    }
  }

  const redo = () => {
    if (historyIndex < history.length - 1) {
      setHistoryIndex(prevIndex => prevIndex + 1)
    }
  }

  const inchesToPixels = (inches) => Math.round(inches * dpi)
  const pixelsToInches = (pixels) => pixels / dpi

  const handleResize = (widthInches, heightInches) => {
    const width = inchesToPixels(widthInches)
    const height = inchesToPixels(heightInches)
    setCanvasSize({ width, height })
  }

  const saveCanvas = () => {
    // Implement save functionality here
    console.log("Saving canvas to profile...")
  }

  const exportCanvas = () => {
    const canvas = canvasRef.current
    if (canvas) {
      const dataUrl = canvas.toDataURL('image/png')
      const link = document.createElement('a')
      link.download = 'canvas-export.png'
      link.href = dataUrl
      link.click()
    }
  }

  const bind = useGesture(
    {
      onDrag: ({ delta: [dx, dy] }) => {
        setPan(prevPan => ({
          x: prevPan.x + dx,
          y: prevPan.y + dy
        }))
      },
      onPinch: ({ offset: [d], origin: [ox, oy], event }) => {
        event.preventDefault()
        setZoom(d)
        // Adjust pan to zoom around the pinch point
        setPan(prevPan => ({
          x: ox - (ox - prevPan.x) * d / zoom,
          y: oy - (oy - prevPan.y) * d / zoom
        }))
      },
    },
    {
      target: containerRef,
      eventOptions: { passive: false },
    }
  )

  const renderRuler = (orientation) => {
    const size = orientation === 'horizontal' ? canvasSize.width : canvasSize.height
    const ticks = []
    const step = inchesToPixels(1) // 1 inch
    for (let i = 0; i <= size; i += step) {
      const position = i * zoom
      const label = Math.floor(pixelsToInches(i))
      ticks.push(
        <div
          key={i}
          className={`absolute bg-gray-400 ${
            orientation === 'horizontal' ? 'h-2 top-0' : 'w-2 left-0'
          }`}
          style={{
            [orientation === 'horizontal' ? 'left' : 'top']: `${position}px`,
            [orientation === 'horizontal' ? 'width' : 'height']: '1px',
          }}
        >
          <span className="absolute text-xs text-gray-600" style={{
            [orientation === 'horizontal' ? 'top' : 'left']: '8px',
            [orientation === 'horizontal' ? 'left' : 'top']: '-6px',
            transform: orientation === 'vertical' ? 'rotate(-90deg)' : 'none',
          }}>
            {label}
          </span>
        </div>
      )
    }
    return ticks
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-r from-blue-400 to-purple-500">
      <header className="flex items-center justify-between p-4 bg-white/10 text-white">
        <div className="flex items-center space-x-4">
            <Dropdown className="md:hidden" visible={mobileMenuOpen} onShow={() => setMobileMenuOpen(!mobileMenuOpen)}>
                <DropdownToggle>
                        <MenuIcon className="h-6 w-6" />
                </DropdownToggle>
                <DropdownMenu>
                    <DropdownItem href="#" onClick={undo}>
                        <UndoIcon className="mr-2 h-4 w-4" />
                        <span>Undo</span>
                    </DropdownItem>
                    <DropdownItem href="#" onClick={redo}>
                        <RedoIcon className="mr-2 h-4 w-4" />
                        <span>Redo</span>
                    </DropdownItem>
                    <DropdownDivider/>
                    <DropdownItem href="#" onClick={saveCanvas}>
                        <SaveIcon className="mr-2 h-4 w-4" />
                        <span>Save</span>
                    </DropdownItem>
                    <DropdownItem href="#" onClick={exportCanvas}>
                        <DownloadIcon className="mr-2 h-4 w-4" />
                        <span>Export</span>
                    </DropdownItem>
                </DropdownMenu>
            </Dropdown>
            <Dropdown visible={fileMenuOpen} onShow={() => setFileMenuOpen(!fileMenuOpen)}>
                <DropdownToggle>
                  File
                </DropdownToggle>
                <DropdownMenu>
                    <DropdownItem href="#" className="flex" onClick={saveCanvas}>
                        <SaveIcon className="mr-2 h-4 w-4" /> 
                        <span>Save</span>
                    </DropdownItem>
                    <DropdownItem href="#"className="flex" onClick={exportCanvas}>
                        <DownloadIcon className="mr-2 h-4 w-4" />
                        <span>Export</span>
                    </DropdownItem>
                </DropdownMenu>
            </Dropdown>
            <Dropdown visible={resizeMenuOpen} onShow={() => setResizeMenuOpen(!resizeMenuOpen)}>
                <DropdownToggle>
                    Resize
                </DropdownToggle>
                <DropdownMenu>
                    <DropdownItem href="#" onSelect={() => handleResize(8.5, 11)}>
                        <span>Letter (8.5 x 11)</span>
                    </DropdownItem>
                    <DropdownItem href="#" onSelect={() => handleResize(11, 17)}>
                        <span>Tabloid (11 x 17)</span>
                    </DropdownItem>
                    <DropdownItem href="#" onSelect={() => handleResize(18, 24)}>
                        <span>Poster (18 x 24)</span>
                    </DropdownItem>
                    <DropdownDivider/>
                        <DropdownItem href="#">
                            <label htmlFor="custom-width">Width (inches)</label>
                            <input
                              id="custom-width"
                              type="number"
                              min="1"
                              step="0.1"
                              onChange={(e) => handleResize(parseFloat(e.target.value), canvasSize.height / dpi)}
                            />
                        </DropdownItem>
                        <DropdownItem href="#">
                            <label htmlFor="custom-height">Height (inches)</label>
                            <input
                            id="custom-height"
                            type="number"
                            min="1"
                            step="0.1"
                            onChange={(e) => handleResize(canvasSize.width / dpi, parseFloat(e.target.value))}
                            />
                        </DropdownItem>
                        <DropdownItem href="#">
                            <label htmlFor="dpi">DPI</label>
                            <input
                              id="dpi"
                              type="number"
                              min="72"
                              max="600"
                              value={dpi}
                              onChange={(e) => setDpi(parseInt(e.target.value))}
                            />
                        </DropdownItem>
                </DropdownMenu>
            </Dropdown>
        </div>
        <div className="hidden md:flex items-center space-x-4">
          <button size="icon" onClick={undo}>
            <UndoIcon className="h-5 w-5" />
          </button>
          <button size="icon" onClick={redo}>
            <RedoIcon className="h-5 w-5" />
          </button>
          <button size="icon">
            <RefreshCwIcon className="h-5 w-5" />
          </button>
          <div className="bg-green-500 rounded-full w-8 h-8 flex items-center justify-center">
            F
          </div>
          <button size="icon">
            <PlusIcon className="h-5 w-5" />
          </button>
          <button size="icon">
            <ShareIcon className="h-5 w-5" />
          </button>
        </div>
      </header>
      <div className="flex flex-1 overflow-hidden">
        <aside className="w-64 bg-gray-800 text-white p-4 space-y-4">
          <input placeholder="Search images by keyword, tags, color..." />
          <button className="w-full bg-purple-600 hover:bg-purple-700" onClick={() => fileinputRef.current?.click()}>
            Upload PNG files
          </button>
          <input
            type="file"
            ref={fileinputRef}
            className="hidden"
            onChange={handleFileChange}
            accept=".png"
            multiple
          />
          <div className="grid grid-cols-3 gap-2">
            {images.map((image, index) => (
              <img
                key={index}
                src={image}
                alt={`Uploaded ${index}`}
                className="w-full h-auto object-cover cursor-pointer"
                onDoubleClick={() => handleImageDoubleClick(image)}
              />
            ))}
          </div>
          {selectedImage && (
            <div className="mt-4 space-y-2">
              <label>Width</label>
              <input
                type="number"
                value={selectedImage.width}
                onChange={(e) => updateSelectedImage({ width: parseInt(e.target.value) })}
              />
              <label>Height</label>
              <input
                type="number"
                value={selectedImage.height}
                onChange={(e) => updateSelectedImage({ height: parseInt(e.target.value) })}
              />
              <label>Rotation</label>
              <div className="flex space-x-2">
                {[90, 180, 270, 360].map((degree) => (
                  <button key={degree} onClick={() => updateSelectedImage({ rotation: degree })}>
                    {degree}°
                  </button>
                ))}
              </div>
              <div className="flex space-x-2">
                <button onClick={() => updateSelectedImage({ flipX: !selectedImage.flipX })}>
                  <FlipHorizontalIcon className="h-4 w-4" />
                </button>
                <button onClick={() => updateSelectedImage({ flipY: !selectedImage.flipY })}>
                  <FlipVerticalIcon className="h-4 w-4" />
                </button>
              </div>
              <button onClick={duplicateSelectedImage} className="w-full">
                Duplicate Image
              </button>
            </div>
          )}
        </aside>
        <main className="flex-1 p-4 bg-gray-100 overflow-hidden">
          <div className="relative w-full h-full" ref={containerRef} {...bind}>
            <div className="absolute left-8 top-0 right-0 h-8 bg-white">
              {renderRuler('horizontal')}
            </div>
            <div className="absolute left-0 top-8 bottom-0 w-8 bg-white">
              {renderRuler('vertical')}
            </div>
            <div className="absolute left-8 top-8 right-0 bottom-0 overflow-hidden">
              <canvas
                ref={canvasRef}
                width={canvasSize.width}
                height={canvasSize.height}
                className="bg-white cursor-pointer"
                style={{
                  transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
                  transformOrigin: '0 0',
                }}
                onClick={handleCanvasClick}
              />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default GangsheetBuilderPOC;