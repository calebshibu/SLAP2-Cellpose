% Define input and output paths

roiThickness = 6;

[fn, dr] = uigetfile('*REFERENCE*.tif');
input = [dr fn];
output = [dr 'CELLPOSE'];

origpath = pwd;

% Define the path to the GitHub project
CPpath = 'C:\Users\aind_ophys\Documents\GitHub\SLAP2-Cellpose';

% Define the path to the Python virtual environment activation script
python_env_path = [CPpath filesep 'cellpose'];

% Change directory to the GitHub project folder
cd(CPpath);

% Construct the command to activate the virtual environment and run the Python script
command = sprintf('"%s\\Scripts\\activate" && python "%s\\run.py" --input "%s" --output "%s"', python_env_path, CPpath, input, output);

% Call the system command
status = system(command);

% image operations to convert masks to outlines
A = ScanImageTiffReader([output filesep 'masks_pred.tif']);
orig = ScanImageTiffReader(input);
orig = orig.data;
masks = A.data;
nZ = size(masks,3);

%only consider planes 4:end-3, to ensure we have context for motion
%correction
nMasks = max(masks,[],[1 2]);
nMasks([1:3, end-2:end]) = 0;
sMasks = sum(masks>0, [1 2]);
sMasks(nMasks~=max(nMasks)) = 0;

zix = find(sMasks == max(sMasks), 1, 'first');

ROIs = zeros(size(masks, [1 2]));
    nmasks = max(masks(:,:,zix),[], 'all');
    O = orig(:,:,zix);
    Os = imgaussfilt(O, [1.5 1.5]);
    for mix = 1:nmasks
        M = masks(:,:,zix)==mix;
        border = M & ~imerode(M, ones(3));

        ROI = imdilate(border, strel('disk', roiThickness));
        
        %adaptive threshold
        thresh = prctile(Os(ROI), 95)/10;
        ROI = ROI & Os>thresh;

        ROIs(ROI) = mix;
    end