/*
 * Source code from https://github.com/arskov/multipart-x-mixed-replace-java-player
 * Author: Arseny Kovalchuk
 * 
 */

package levus.gui.helper;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

/**
 * Implementation of a connection to motion jpeg (multipart/x-mixed-replace) stream, and using it as an Itarable like this:
 *   <pre>
 *   public static void main(String... strings) {
 *       VideoSource src = new VideoSource("http://91.85.203.9/axis-cgi/mjpg/video.cgi");
 *       try {
 *           src.connect();
 *           for (byte[] img : src) {
 *               Files.write(Paths.get("c:/tmp/mjpeg/" + UUID.randomUUID().toString() + ".jpg"), img);
 *           }
 *       } catch (IOException e) {
 *           e.printStackTrace();
 *       }
 *   }
 *   </pre>
 * 
 * 
 * @author Arseny Kovalchuk<br/><a href="http://www.linkedin.com/in/arsenykovalchuk/">LinkedIn&reg; Profile</a>
 *
 */
public class VideoSource implements Iterable<byte[]> {
    private final static String MULTIPART_MIXED_REPLACE = "multipart/x-mixed-replace";
    private final static String BOUNDARY_PART = "boundary=";
    private final static String CONTENT_TYPE_HEADER = "content-length";

    private final String urlString;
    private String boundaryPart;
    private HttpURLConnection conn;
    private ImagesIterator iterator;

    public VideoSource(String url) {
        this.urlString = url;
    }

    public void connect() throws IOException {
        URL url = new URL(this.urlString);
        conn = (HttpURLConnection) url.openConnection();
        conn.setReadTimeout(0);
        conn.connect();
        String contentType = conn.getContentType();
        if (contentType != null && !contentType.startsWith(MULTIPART_MIXED_REPLACE))
            throw new IOException("Unsupported Content-Type: " + contentType);

        assert contentType != null;
        boundaryPart = contentType.substring(contentType.indexOf(BOUNDARY_PART)
                + BOUNDARY_PART.length());
        //System.out.println("Stream content type header: " + contentType);
        System.out.println("Conexión establecida con: " + this.urlString);
        System.out.println("Tipo de contenido: " + contentType);
    }
    
    public void disconnect() {
        if (this.conn != null)
            this.conn.disconnect();
        if (this.iterator != null) {
            this.iterator.close();
            this.iterator = null;
        }
    }

    @Override
    public Iterator<byte[]> iterator() {
        try {
            return getIterator();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    public byte[] getNextFrame() throws IOException {
        iterator = (ImagesIterator) getIterator();
        if (iterator.hasNext()) {
            return iterator.next();
        }
        return null; 
    }

    public Iterator<byte[]> getIterator() throws IOException {
        if (this.iterator == null) {
            this.iterator = new ImagesIterator(boundaryPart, conn);
        }
        return this.iterator;
    }

    private static class ImagesIterator implements Iterator<byte[]> {

        private byte LF = 0x0A;
        private byte CR = 0x0D;

        private String boundary;
        
        private InputStream stream;
        private boolean hasNext;
        private HttpURLConnection conn;

        ImagesIterator(String boundaryPart, HttpURLConnection conn) throws IOException {
            // Some cameras provide Content-Type header with ; boundary=--myboundary,
            // then they use it as is without prefixing it with --
            this.boundary = boundaryPart.startsWith("--") ? boundaryPart : "--" + boundaryPart;
            this.conn = conn;
            this.stream = new BufferedInputStream(conn.getInputStream(), 8192);
            this.hasNext = true;
        }
        
        private String readLine() throws IOException {
            int counter = 0, capacity = 512;
            byte[] buffer = new byte[capacity];
            StringBuilder stringBuffer = new StringBuilder(512);
            readBuffer:
            for (;;) {
                stream.mark(capacity);
                int bytes = stream.read(buffer, 0, capacity);
                int i = 0;
                
                findCRLF:
                for (; i < capacity; i++) {
                    if (buffer[i] == LF) {
                        stream.reset();
                        stream.read(buffer, 0, i + 1);
                        stringBuffer.append(new String(buffer, 0, i));
                        return stringBuffer.toString().trim();
                    }
                }
                stringBuffer.append(new String(buffer, 0, capacity));
            }
            
        }
        
        private void readUntilBoundary() throws IOException, InterruptedException {
            for(;;) {
                String s = readLine();
                if (boundary.equals(s) || !hasNext) {
                    break;
                } else if (s.equals(boundary + "--")) /* end of stream */{
                    hasNext = false;
                    break;
                }
            } 
        }
        
        /**
         * Reads headers from the stream
         * @return
         * @throws IOException
         * @throws InterruptedException 
         */
        private Map<String, String> readHeaders() throws IOException, InterruptedException {
            String line = null;
            Map<String, String> headers = new HashMap<>();
            for(;;) {
                line = readLine();
                if (line.trim().isEmpty()) {
                    return headers;
                } else {
                    String[] parts = line.split(": ");
                    headers.put(parts[0].toLowerCase(), parts[1]);
                }
            }
        }

        @Override
        public boolean hasNext() {
            synchronized (this)  {
                return this.hasNext;
            }
        }

        /**
         * Note! Throws RuntimeException(IOException | InterruptedException).
         * 
         * It's usable especially in case of InterruptedException, when this source
         * is being to use in the thread like StreamThread
         */
        @Override
        public byte[] next() {
            synchronized (this) {
                byte[] buffer = new byte[0];
                try {
                    readUntilBoundary();
                    Map<String, String> headers = readHeaders();
                    String contentLength = headers.get(CONTENT_TYPE_HEADER);
                    int length = 0;
                    try {
                        length = Integer.parseInt(contentLength);
                    } catch (NumberFormatException e) {
                        return buffer;
                    }
                    buffer = new byte[length];
                    int bytes = 0;
                    while (bytes < length) {
                        bytes += stream.read(buffer, bytes, length - bytes);
                    }
                    //System.out.println("Bytes read: " + bytes);
                    
                    return buffer;
                } catch (IOException | InterruptedException e) {
                    //e.printStackTrace();
                    // see StreamThread how it's to be used.
                    return null;
                }
            }
        }

        @Override
        public void remove() {
            // do nothing
        }
        
        /**
         * Closes input stream
         */
        synchronized void close() {
            this.hasNext = false;
            try {
                this.stream.close();
            } catch (IOException e) {
                System.out.println("Error closing stream");
                e.printStackTrace();
            }
        }

    }
    
}