param(
    [Parameter(Mandatory=$true)][string]$InputPath,
    [Parameter(Mandatory=$true)][string]$OutputPath
)

Add-Type -AssemblyName System.Drawing

Add-Type -ReferencedAssemblies @("System.Drawing.dll") -TypeDefinition @"
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

public static class DreamEffect {
    static double Clamp01(double v) { return v < 0 ? 0 : (v > 1 ? 1 : v); }
    static byte B(double v) { return (byte)Math.Max(0, Math.Min(255, Math.Round(v))); }
    static double Smooth(double e0, double e1, double x) {
        if (e0 == e1) return 0;
        double t = Clamp01((x - e0) / (e1 - e0));
        return t * t * (3 - 2 * t);
    }
    static double Glow(double xn, double yn, double cx, double cy, double rx, double ry, double strength) {
        double dx = (xn - cx) / rx;
        double dy = (yn - cy) / ry;
        double d2 = dx * dx + dy * dy;
        if (d2 >= 1) return 0;
        return strength * Math.Pow(1 - d2, 2.25);
    }

    public static void Apply(string inputPath, string outputPath) {
        using (Bitmap src0 = (Bitmap)Image.FromFile(inputPath))
        using (Bitmap src = new Bitmap(src0.Width, src0.Height, PixelFormat.Format32bppArgb))
        using (Graphics g = Graphics.FromImage(src)) {
            g.DrawImage(src0, 0, 0, src0.Width, src0.Height);

            int w = src.Width;
            int h = src.Height;
            Rectangle rect = new Rectangle(0, 0, w, h);
            BitmapData data = src.LockBits(rect, ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
            int stride = data.Stride;
            int len = Math.Abs(stride) * h;
            byte[] px = new byte[len];
            Marshal.Copy(data.Scan0, px, 0, len);

            for (int y = 0; y < h; y++) {
                double yn = y / (double)(h - 1);
                for (int x = 0; x < w; x++) {
                    double xn = x / (double)(w - 1);
                    int i = y * stride + x * 4;
                    double b = px[i + 0];
                    double gch = px[i + 1];
                    double r = px[i + 2];
                    double a = px[i + 3];
                    double lum = (0.2126 * r + 0.7152 * gch + 0.0722 * b) / 255.0;

                    double sky = (1.0 - Smooth(0.31, 0.58, yn)) * Smooth(0.08, 0.94, xn);
                    sky *= Smooth(0.07, 0.56, lum);

                    double dist = Math.Abs(xn - 0.50);
                    double road = Smooth(0.50, 0.98, yn) * (1.0 - Smooth(0.03, 0.31, dist));
                    road *= Smooth(0.10, 0.58, lum);

                    double mist = (1.0 - Smooth(0.12, 0.40, Math.Abs(xn - 0.50))) *
                                  (1.0 - Smooth(0.26, 0.76, Math.Abs(yn - 0.57))) * 0.30;

                    double pink = Math.Min(0.76, sky * 0.80 + road * 0.66 + mist);

                    double warm = 0;
                    warm = Math.Max(warm, Glow(xn, yn, 260.0 / w, 675.0 / h, 0.045, 0.060, 0.95));
                    warm = Math.Max(warm, Glow(xn, yn, 1050.0 / w, 770.0 / h, 0.052, 0.065, 0.88));

                    double building = Smooth(0.12, 0.92, yn);
                    double edgeLight = Smooth(0.21, 0.55, lum) * building;
                    if (edgeLight > 0 && (xn < 0.38 || xn > 0.62 || yn > 0.62)) {
                        warm = Math.Max(warm, edgeLight * 0.34);
                    }
                    warm = Math.Min(0.88, warm);

                    double basePurple = 0.28 + 0.22 * Smooth(0.03, 0.45, lum);
                    double nr = r * (1.0 - basePurple) + 88.0 * basePurple;
                    double ng = gch * (1.0 - basePurple) + 42.0 * basePurple;
                    double nb = b * (1.0 - basePurple) + 104.0 * basePurple;

                    nr = nr * (1.0 - pink) + (212.0 + 70.0 * lum) * pink;
                    ng = ng * (1.0 - pink) + 48.0 * pink;
                    nb = nb * (1.0 - pink) + (148.0 + 40.0 * lum) * pink;

                    nr = nr * (1.0 - warm) + 255.0 * warm;
                    ng = ng * (1.0 - warm) + 118.0 * warm;
                    nb = nb * (1.0 - warm) + 64.0 * warm;

                    double ink = 0.53 + 0.47 * lum;
                    nr *= ink;
                    ng *= ink;
                    nb *= ink;

                    if (lum < 0.045) {
                        nr *= 0.42;
                        ng *= 0.35;
                        nb *= 0.50;
                    }

                    px[i + 0] = B(nb);
                    px[i + 1] = B(ng);
                    px[i + 2] = B(nr);
                    px[i + 3] = B(a);
                }
            }

            Marshal.Copy(px, 0, data.Scan0, len);
            src.UnlockBits(data);
            src.Save(outputPath, ImageFormat.Png);
        }
    }
}
"@

[DreamEffect]::Apply($InputPath, $OutputPath)
