# This script will build all of the binary encoders and decoders included with
# the test harness, provided you have the required libraries installed at the
# correct locations. Tweaking may be required.

cd encoders
echo "Compiling yuvjpeg..."
gcc -O3 yuvjpeg.c -std=c99 -I../../libjpeg-turbo-1.5.0/ ../../libjpeg-turbo-1.5.0/.libs/libjpeg.a -o yuvjpeg || { echo 'Failed!' ; exit 1; }
echo "Compiling yuvmozjpeg..."
gcc -O3 yuvmozjpeg.c -std=c99 -I../../mozjpeg/ ../../mozjpeg/.libs/libjpeg.a -lm -o yuvmozjpeg || { echo 'Failed!' ; exit 1; }
echo "Compiling yuvjxr..."
gcc -O3 yuvjxr.c -D__ANSI__ -I../../jxrlib/jxrtestlib -I../../jxrlib/common/include -I../../jxrlib/jxrgluelib -I../../jxrlib/image/sys ../../jxrlib/build/libjxrglue.a ../../jxrlib/build/libjpegxr.a -o yuvjxr -lm || { echo 'Failed!' ; exit 1; }
echo "Compiling yuvwebp..."
gcc -O3 yuvwebp.c -o yuvwebp -std=c99 -I../../libwebp-0.5.1/src/ ../../libwebp-0.5.1/src/.libs/libwebp.a -lm -pthread || { echo 'Failed!' ; exit 1; }
cd ..

cd decoders
echo "Compiling jpegyuv..."
gcc -O3 jpegyuv.c -std=c99 -I../../libjpeg-turbo-1.5.0/ ../../libjpeg-turbo-1.5.0/.libs/libjpeg.a -o jpegyuv || { echo 'Failed!' ; exit 1; }
echo "Compiling jxryuv..."
gcc -O3 jxryuv.c -I../../jxrlib/jxrtestlib -I../../jxrlib/common/include -I../../jxrlib/jxrgluelib -I../../jxrlib/image/sys -D__ANSI__ ../../jxrlib/build/libjxrglue.a ../../jxrlib/build/libjpegxr.a -lm -o jxryuv || { echo 'Failed!' ; exit 1; }
echo "Compiling webpyuv..."
gcc -O3 webpyuv.c -std=c99 -I../../libwebp-0.5.1/src/ ../../libwebp-0.5.1/src/.libs/libwebp.a -lm -pthread -o webpyuv || { echo 'Failed!' ; exit 1; }
cd ..

cd tests/msssim
echo "Compiling iqa library..."
cd iqa-lib
RELEASE=1 make
cd ..
echo "Compiling msssim..."
gcc -O3 -o msssim -Iiqa-lib/include -I../common ../common/y4m_input.c ../common/vidinput.c msssim.c iqa-lib/build/release/libiqa.a -lm || { echo 'Failed!' ; exit 1; }
cd ../..

cd tests/ssim
echo "Compiling ssim..."
gcc -O3 -o ssim -I../common ../common/vidinput.c ../common/y4m_input.c ssim.c -lm || { echo 'Failed!' ; exit 1; }
cd ../..

cd tests/psnrhvsm
echo "Compiling psnrhvsm..."
gcc -O3 -o psnrhvsm -I../common ../common/vidinput.c ../common/y4m_input.c psnrhvs.c -lm || { echo 'Failed!' ; exit 1; }
cd ../..

echo "Success building all encoders and decoders."
exit 0
