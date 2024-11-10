export const getStringColor = (string: string): string => {
    var hash = 0;

    for (var i = 0; i < string.length; i++)
    {
        hash = string.charCodeAt(i) + ((hash << 5) - hash);
        hash = hash & hash;
    }

    var rgb = [0, 0, 0];

    for (var i = 0; i < 3; i++)
    {
        var value = (hash >> (i * 8)) & 255;
        rgb[i] = value;
    }

    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
};

export const apiUrl = 'http://localhost:5000';
